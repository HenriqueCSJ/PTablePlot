# Element Properties Visualization

A PyQt5 application that visualizes element properties such as ionization energy and atomic radius. It also displays a periodic table highlighting the selected element.

## Features

- **Interactive Plotting**: Visualize ionization energy and atomic radius against atomic number.
- **Custom Periodic Table**: Displays a periodic table with the selected element highlighted.
- **Interactive Tooltips**: Hover over data points to see detailed information about each element.
- **User Controls**: Slider to select atomic number and checkboxes to toggle displayed properties.
- **Responsive GUI**: Adjustable sizes of the plots and periodic table within the application window.

## Screenshots

*(You can add screenshots of the application here to showcase the interface and features.)*

## Installation

### Prerequisites

- **Python 3.x**
- **PyQt5**
- **Matplotlib**
- **Mendeleev**

### Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install PyQt5 matplotlib mendeleev
```

Alternatively, if you are using Anaconda:

```bash
conda install pyqt matplotlib
pip install mendeleev
```

### Download the Code

Clone the repository or download the script directly:

```bash
git clone https://github.com/HenriqueCSJ/PTablePlot.git
```

## Usage

Navigate to the directory containing the script and run it using Python:

```bash
python PTablePlot.py
```

## How to Use the Application

1. **Select Atomic Number**: Use the slider at the bottom to select an atomic number (Z). The default value is 10.

2. **Toggle Properties**: Use the checkboxes to select which properties to display:
   - **Ionization Energy**
   - **Atomic Radius**

3. **Interact with Plots**:
   - **Hover**: Move your cursor over data points to see tooltips with detailed information.
   - **Zoom and Pan**: Use the navigation toolbar to zoom in/out or pan the plots.
   - **Save Figures**: Use the toolbar to save the current plots as images.

4. **Periodic Table**:
   - The periodic table on the right highlights the selected element in yellow.
   - The element symbol is displayed in each cell.

## Code Overview

### `elements_details` Dictionary

- Collects data for elements with atomic numbers from 1 to 118.
- Stores properties such as ionization energy, atomic radius, symbol, name, electron configuration, electron affinity, group ID, and period.

### `MyMplCanvas` Class

- Inherits from `FigureCanvas`.
- Responsible for plotting the element properties.
- Uses primary (`self.axes`) and secondary (`self.axes2`) y-axes to plot multiple properties.
- Implements interactive tooltips when hovering over data points.

### `PeriodicTableCanvas` Class

- Inherits from `FigureCanvas`.
- Displays a custom periodic table with the selected element highlighted.
- Calculates positions of elements based on their group and period.
- Uses Matplotlib patches to draw the periodic table.

### `ApplicationWindow` Class

- Inherits from `QMainWindow`.
- Combines all components into the main application window.
- Manages layouts and user controls (slider and checkboxes).
- Updates plots and periodic table based on user interaction.

## Customization

### Adjusting Plot Sizes

- Modify the `width` and `height` parameters in the `MyMplCanvas` and `PeriodicTableCanvas` classes to change the sizes of the plots.

  ```python
  # Example: Increase the size of the property plot
  self.canvas = MyMplCanvas(self.main_widget, width=8, height=6, dpi=100)
  ```

### Changing Appearance

- Customize colors, fonts, and styles within the plotting methods.
- For example, to change the highlight color of the selected element in the periodic table:

  ```python
  if Z == atomic_number:
      color = "lightgreen"  # Change highlight color to light green
  ```

### Adding More Element Properties

- Extend the `elements_details` dictionary to include additional properties.
- Update the plotting methods in `MyMplCanvas` to visualize the new properties.
- Add corresponding checkboxes or controls in the `ApplicationWindow` class.

## Dependencies

- **Python 3.x**: The programming language used.
- **PyQt5**: For creating the graphical user interface.
- **Matplotlib**: For plotting graphs and creating the periodic table visualization.
- **Mendeleev**: For accessing detailed information about chemical elements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **[Mendeleev Library](https://github.com/lmmentel/mendeleev)**: For providing comprehensive data on chemical elements.
- **[Matplotlib](https://matplotlib.org/)**: For making plotting in Python easy and interactive.
- **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro)**: For enabling GUI development in Python.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss improvements, bug fixes, or new features.
