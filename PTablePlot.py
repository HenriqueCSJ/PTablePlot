import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSlider,
    QCheckBox,
    QLabel,
    QGroupBox,
    QGridLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mendeleev import element
import matplotlib.patches as patches

# Use a built-in matplotlib style
plt.style.use("ggplot")

# Gather element details
elements_details = {}
for Z in range(1, 119):
    el = element(Z)

    # Ionization Energy
    ion_energy = el.ionenergies.get(1, None)
    if ion_energy is None:
        if Z == 1:
            ion_energy = 13.5984  # eV for Hydrogen
        elif Z == 2:
            ion_energy = 24.5874  # eV for Helium

    # Atomic Radius
    atomic_radius = el.covalent_radius_pyykko
    if atomic_radius is None:
        atomic_radius = el.covalent_radius_slater
    if atomic_radius is None:
        if Z == 1:
            atomic_radius = 31.5  # pm, approximate for Hydrogen
        elif Z == 2:
            atomic_radius = 28.0  # pm, approximate for Helium

    elements_details[Z] = {
        "ion_energy": ion_energy,
        "symbol": el.symbol,
        "name": el.name,
        "ec": el.econf,
        "atomic_radius": atomic_radius,
        "electron_affinity": el.electron_affinity,
        "group_id": el.group_id,
        "period": el.period,
    }


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=7, height=5, dpi=100):
        # Enable constrained layout to handle axis labels properly
        self.fig = Figure(figsize=(width, height), dpi=dpi, constrained_layout=True)
        super().__init__(self.fig)
        self.setParent(parent)

        self.axes = self.fig.add_subplot(111)
        self.axes2 = self.axes.twinx()

        self.show_ionization = False
        self.show_radius = True
        self.current_atomic_number = 1  # Initialize current atomic number

        # Connect the motion event for tooltips
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)

        self.plot_initial_figure()

    def plot_initial_figure(self):
        self.update_figure(self.current_atomic_number)

    def update_figure(self, atomic_number):
        self.current_atomic_number = atomic_number
        self.axes.clear()
        self.axes2.clear()

        # Prepare data
        atomic_numbers_ie = []
        ion_energies = []
        if self.show_ionization:
            for z in range(1, atomic_number + 1):
                ion_energy = elements_details[z]["ion_energy"]
                if ion_energy is not None:
                    atomic_numbers_ie.append(z)
                    ion_energies.append(ion_energy)
            if ion_energies:
                (line1,) = self.axes.plot(
                    atomic_numbers_ie,
                    ion_energies,
                    marker="o",
                    linestyle="-",
                    label="Ionization Energy (eV)",
                    color="#1f77b4",
                )
                self.axes.set_ylabel(
                    "First Ionization Energy (eV)", color="#1f77b4", fontsize=12
                )
                self.axes.tick_params(axis="y", colors="#1f77b4")
                self.axes.legend(loc="upper left")
                # Ensure primary y-axis label is on the left
                self.axes.yaxis.set_label_position("left")
                self.axes.yaxis.tick_left()

        atomic_numbers_ar = []
        atomic_radii = []
        if self.show_radius:
            for z in range(1, atomic_number + 1):
                atomic_radius = elements_details[z]["atomic_radius"]
                if atomic_radius is not None:
                    atomic_numbers_ar.append(z)
                    atomic_radii.append(atomic_radius)
            if atomic_radii:
                (line2,) = self.axes2.plot(
                    atomic_numbers_ar,
                    atomic_radii,
                    marker="s",
                    linestyle="--",
                    label="Atomic Radius (pm)",
                    color="#ff7f0e",
                )
                self.axes2.set_ylabel(
                    "Atomic Radius (pm)", color="#ff7f0e", fontsize=12
                )
                self.axes2.tick_params(axis="y", colors="#ff7f0e")
                self.axes2.legend(loc="upper right")
                # Ensure secondary y-axis label is on the right
                self.axes2.yaxis.set_label_position("right")
                self.axes2.yaxis.tick_right()

        # Set the title using a larger font size
        if atomic_number in elements_details:
            current_element = elements_details[atomic_number]
            title = f"Z={atomic_number} ({current_element['symbol']}: {current_element['name']})\nElectron Configuration: {current_element['ec']}"
        else:
            title = "Element Properties"
        self.axes.set_title(title, fontsize=14, fontweight="bold")

        self.axes.set_xlabel("Atomic Number (Z)", fontsize=12)
        self.axes.grid(True)

        self.draw()

    def toggle_ionization(self, state):
        self.show_ionization = state
        self.update_figure(self.current_atomic_number)

    def toggle_radius(self, state):
        self.show_radius = state
        self.update_figure(self.current_atomic_number)

    def on_hover(self, event):
        # Show tooltips when hovering over data points
        if event.inaxes == self.axes or event.inaxes == self.axes2:
            for line in self.axes.get_lines() + self.axes2.get_lines():
                cont, ind = line.contains(event)
                if cont:
                    z = line.get_xdata()[ind["ind"][0]]
                    element = elements_details[int(z)]
                    text = f"{element['symbol']} (Z={z})\n"
                    if line.get_label() == "Ionization Energy (eV)":
                        value = element["ion_energy"]
                        text += f"Ionization Energy: {value:.2f} eV"
                    elif line.get_label() == "Atomic Radius (pm)":
                        value = element["atomic_radius"]
                        text += f"Atomic Radius: {value:.2f} pm"
                    if not hasattr(self, "tooltips"):
                        self.tooltips = event.inaxes.annotate(
                            text,
                            xy=(event.xdata, event.ydata),
                            xytext=(20, 20),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"),
                        )
                    else:
                        self.tooltips.set_text(text)
                        self.tooltips.xy = (event.xdata, event.ydata)
                    self.tooltips.set_visible(True)
                    self.draw()
                    return
        if hasattr(self, "tooltips"):
            if self.tooltips.get_visible():
                self.tooltips.set_visible(False)
                self.draw()


class PeriodicTableCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        self.current_atomic_number = 1  # Initialize current atomic number
        self.plot_table(self.current_atomic_number)

    def plot_table(self, atomic_number):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis("off")

        # Define the positions of the elements
        positions = {}
        for Z in elements_details:
            el = elements_details[Z]
            group = el["group_id"] if el["group_id"] else 0
            period = el["period"] if el["period"] else 0
            if group and period:
                x = group
                y = period
            elif Z >= 57 and Z <= 71:  # Lanthanides
                x = (Z - 57) + 3
                y = 8
            elif Z >= 89 and Z <= 103:  # Actinides
                x = (Z - 89) + 3
                y = 9
            else:
                continue
            positions[Z] = (x, y)

        # Draw the elements
        for Z, (x, y) in positions.items():
            el = elements_details[Z]
            color = "white"
            edgecolor = "black"
            if Z == atomic_number:
                color = "yellow"
            rect = patches.Rectangle(
                (x - 0.5, y - 0.5),
                1,
                1,
                linewidth=1,
                edgecolor=edgecolor,
                facecolor=color,
            )
            ax.add_patch(rect)
            ax.text(x, y, el["symbol"], ha="center", va="center", fontsize=8)
            # Optionally, display atomic number
            # ax.text(x, y - 0.3, str(Z), ha='center', va='center', fontsize=6)

        ax.set_xlim(0.5, 18.5)
        ax.set_ylim(10.5, 0.5)
        ax.set_aspect("equal")
        self.draw()

    def update_table(self, atomic_number):
        self.current_atomic_number = atomic_number
        self.plot_table(self.current_atomic_number)


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Element Properties Visualization")
        self.setMinimumSize(1000, 600)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Create the main layout
        main_layout = QVBoxLayout(self.main_widget)

        # Create the plot canvases
        self.plot_widget = QWidget()
        plot_layout = QHBoxLayout(self.plot_widget)

        # Property plot canvas
        self.canvas = MyMplCanvas(self.main_widget, width=7, height=5, dpi=100)
        toolbar1 = NavigationToolbar(self.canvas, self)
        canvas_layout = QVBoxLayout()
        canvas_layout.addWidget(toolbar1)
        canvas_layout.addWidget(self.canvas)
        canvas_widget = QWidget()
        canvas_widget.setLayout(canvas_layout)

        # Periodic table canvas
        self.pt_canvas = PeriodicTableCanvas(
            self.main_widget, width=5, height=5, dpi=100
        )
        toolbar2 = NavigationToolbar(self.pt_canvas, self)
        pt_layout = QVBoxLayout()
        pt_layout.addWidget(toolbar2)
        pt_layout.addWidget(self.pt_canvas)
        pt_widget = QWidget()
        pt_widget.setLayout(pt_layout)

        # Add canvases to the plot layout with stretch factors
        plot_layout.addWidget(
            canvas_widget, stretch=3
        )  # Property plot takes more space
        plot_layout.addWidget(pt_widget, stretch=2)  # Periodic table takes less space

        main_layout.addWidget(self.plot_widget)

        # Create a widget for the controls
        controls_widget = QWidget()
        controls_layout = QGridLayout(controls_widget)

        # Slider
        slider_label = QLabel("Select Atomic Number (Z):")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 118)
        self.slider.setValue(10)
        self.slider.valueChanged[int].connect(self.update_plot)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)

        # Slider layout
        slider_layout = QVBoxLayout()
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.slider)

        # Checkboxes
        checkbox_group = QGroupBox("Properties to Display:")
        checkbox_layout = QVBoxLayout()
        self.toggle_ionization = QCheckBox("Ionization Energy")
        self.toggle_ionization.stateChanged.connect(
            lambda state: self.canvas.toggle_ionization(state == Qt.Checked)
        )
        self.toggle_radius = QCheckBox("Atomic Radius")
        self.toggle_radius.setChecked(True)
        self.toggle_radius.stateChanged.connect(
            lambda state: self.canvas.toggle_radius(state == Qt.Checked)
        )
        checkbox_layout.addWidget(self.toggle_ionization)
        checkbox_layout.addWidget(self.toggle_radius)
        checkbox_group.setLayout(checkbox_layout)

        # Add controls to the grid layout
        controls_layout.addLayout(slider_layout, 0, 0)
        controls_layout.addWidget(checkbox_group, 0, 1)

        # Adjust size policies
        controls_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        checkbox_group.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add controls widget to the main layout
        main_layout.addWidget(controls_widget)

        # Initialize the plot with the slider's default value
        self.update_plot(self.slider.value())

    def update_plot(self, value):
        self.canvas.update_figure(value)
        self.pt_canvas.update_table(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.show()
    sys.exit(app.exec_())
