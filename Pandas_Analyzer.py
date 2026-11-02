import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class SalesDataAnalyzer:

    def __init__(self):
        self.data = None
        self.current_figure = None

    # 1. Load Dataset
    def load_data(self):
        print("\n== Load Dataset ==")

        path = input(
            "Enter the path of the dataset (CSV file): "
        ).strip().strip('"')

        if not os.path.isfile(path):
            print("Error: Dataset file not found!")
            return

        try:
            self.data = pd.read_csv(path)
            print("Dataset loaded successfully!")

        except Exception as e:
            print("Error loading dataset:", e)

    # Check Dataset
    def check_data(self):
        if self.data is None:
            print("Please load a dataset first!")
            return False
        return True

    # 2. Explore Data
    def explore_data(self):
        if not self.check_data():
            return

        while True:
            print("\n== Explore Data ==")
            print("1. Display the first 5 rows")
            print("2. Display the last 5 rows")
            print("3. Display column names")
            print("4. Display data types")
            print("5. Display basic info")
            print("6. Back to Main Menu")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                print(self.data.head())

            elif choice == "2":
                print(self.data.tail())

            elif choice == "3":
                print(self.data.columns.tolist())

            elif choice == "4":
                print(self.data.dtypes)

            elif choice == "5":
                self.data.info()

            elif choice == "6":
                return

            else:
                print("Invalid choice! Please try again.")

    # 3. DataFrame Operations
    def dataframe_operations(self):
        if not self.check_data():
            return

        while True:
            print("\n== DataFrame Operations ==")
            print("1. Mathematical Operations")
            print("2. Combine DataFrames")
            print("3. Split DataFrame")
            print("4. Search, Sort and Filter")
            print("5. Aggregate Functions")
            print("6. Statistical Analysis")
            print("7. Create Pivot Table")
            print("8. Back to Main Menu")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.mathematical_operations()

            elif choice == "2":
                self.combine_dataframes()

            elif choice == "3":
                self.split_dataframe()

            elif choice == "4":
                self.search_sort_filter()

            elif choice == "5":
                self.aggregate_functions()

            elif choice == "6":
                self.statistical_analysis()

            elif choice == "7":
                self.create_pivot_table()

            elif choice == "8":
                return

            else:
                print("Invalid choice! Please try again.")

    # Select Numeric Column
    def select_numeric_column(self, message):
        columns = self.data.select_dtypes(
            include=np.number
        ).columns.tolist()

        if not columns:
            print("No numeric columns available!")
            return None

        print("Available numeric columns:", columns)

        column = input(message).strip()

        if column not in columns:
            print("Invalid numeric column name!")
            return None

        return column

    # 3.1 Mathematical Operations
    def mathematical_operations(self):
        column = self.select_numeric_column(
            "Enter numeric column name: "
        )

        if column is None:
            return

        print("\n1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Square")
        print("6. Square Root")
        print("7. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "7":
            return

        values = pd.to_numeric(
            self.data[column], errors="coerce"
        )

        if choice in ("1", "2", "3", "4"):
            try:
                number = float(input("Enter a number: "))

                if choice == "1":
                    result = values + number

                elif choice == "2":
                    result = values - number

                elif choice == "3":
                    result = values * number

                else:
                    if number == 0:
                        print("Cannot divide by zero!")
                        return
                    result = values / number

                print(result)

            except ValueError:
                print("Please enter a valid number!")

        elif choice == "5":
            print(values ** 2)

        elif choice == "6":
            print(np.sqrt(values))

        else:
            print("Invalid choice!")

    # 3.2 Combine DataFrames
    def combine_dataframes(self):
        path = input(
            "Enter the path of the second CSV file: "
        ).strip().strip('"')

        if not os.path.isfile(path):
            print("Second dataset not found!")
            return

        try:
            second_data = pd.read_csv(path)

            print("1. Concatenate DataFrames")
            print("2. Merge DataFrames")
            print("3. Back")

            choice = input("Enter your choice: ").strip()

            if choice == "3":
                return

            if choice == "1":
                result = pd.concat(
                    [self.data, second_data],
                    ignore_index=True,
                    sort=False
                )

            elif choice == "2":
                common_columns = [
                    column for column in self.data.columns
                    if column in second_data.columns
                ]

                if not common_columns:
                    print("No common columns available!")
                    return

                print("Common columns:", common_columns)

                column = input(
                    "Enter column name for merging: "
                ).strip()

                if column not in common_columns:
                    print("Invalid column name!")
                    return

                result = pd.merge(
                    self.data,
                    second_data,
                    on=column,
                    how="inner",
                    suffixes=("_left", "_right")
                )

            else:
                print("Invalid choice!")
                return

            print(result.head())

            save = input(
                "Save combined DataFrame? (yes/no): "
            ).strip().lower()

            if save in ("yes", "y"):
                output = input(
                    "Enter output CSV filename: "
                ).strip()

                if not output:
                    output = "combined_data.csv"

                result.to_csv(output, index=False)
                print("Combined DataFrame saved successfully!")

        except Exception as e:
            print("Error combining DataFrames:", e)

    # 3.3 Split DataFrame
    def split_dataframe(self):
        print("\n1. Split by row count")
        print("2. Split by column value")
        print("3. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "3":
            return

        if choice == "1":
            try:
                size = int(input("Enter rows per part: "))

                if size <= 0:
                    print("Enter a positive number!")
                    return

                for number, start in enumerate(
                    range(0, len(self.data), size), start=1
                ):
                    part = self.data.iloc[start:start + size]

                    part.to_csv(
                        f"split_part_{number}.csv",
                        index=False
                    )

                    print(f"Part {number} saved successfully!")

            except ValueError:
                print("Enter a valid integer!")

        elif choice == "2":
            column = input("Enter column name: ").strip()

            if column not in self.data.columns:
                print("Invalid column name!")
                return

            try:
                for value, group in self.data.groupby(
                    column, dropna=False, sort=False
                ):
                    label = (
                        "missing" if pd.isna(value)
                        else str(value)
                    )

                    label = "".join(
                        char if char.isalnum() or char in "_-"
                        else "_"
                        for char in label
                    )

                    filename = f"split_{label[:40]}.csv"
                    group.to_csv(filename, index=False)

                    print(f"Saved: {filename}")

            except Exception as e:
                print("Error splitting DataFrame:", e)

        else:
            print("Invalid choice!")

    # 3.4 Search, Sort and Filter
    def search_sort_filter(self):
        print("\n1. Search")
        print("2. Sort")
        print("3. Filter")
        print("4. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "4":
            return

        if choice == "1":
            column = input("Enter column name: ").strip()

            if column not in self.data.columns:
                print("Invalid column!")
                return

            value = input("Enter value to search: ")

            result = self.data[
                self.data[column].astype(str) == value
            ]

            print(result)

        elif choice == "2":
            column = input("Enter column name: ").strip()

            if column not in self.data.columns:
                print("Invalid column!")
                return

            order = input(
                "Sort ascending? (yes/no): "
            ).strip().lower()

            result = self.data.sort_values(
                by=column,
                ascending=order in ("yes", "y"),
                na_position="last"
            )

            print(result)

        elif choice == "3":
            column = self.select_numeric_column(
                "Enter numeric column name: "
            )

            if column is None:
                return

            try:
                minimum = float(
                    input("Enter minimum value: ")
                )

                values = pd.to_numeric(
                    self.data[column], errors="coerce"
                )

                print(self.data[values >= minimum])

            except ValueError:
                print("Enter a valid number!")

        else:
            print("Invalid choice!")

    # 3.5 Aggregate Functions
    def aggregate_functions(self):
        column = self.select_numeric_column(
            "Enter numeric column name: "
        )

        if column is None:
            return

        values = pd.to_numeric(
            self.data[column], errors="coerce"
        )

        print("Sum:", values.sum())
        print("Mean:", values.mean())
        print("Minimum:", values.min())
        print("Maximum:", values.max())
        print("Count:", values.count())
        print("Median:", values.median())
        print("Standard Deviation:", values.std())
        print("Variance:", values.var())

    # 3.6 Statistical Analysis
    def statistical_analysis(self):
        numeric_data = self.data.select_dtypes(
            include=np.number
        )

        if numeric_data.empty:
            print("No numeric columns available!")
            return

        print("\nDescriptive Statistics:")
        print(numeric_data.describe())

        print("\nCorrelation Matrix:")
        print(numeric_data.corr())

        print("\nVariance:")
        print(numeric_data.var())

        print("\nSkewness:")
        print(numeric_data.skew())

    # 3.7 Create Pivot Table
    def create_pivot_table(self):
        print("Available columns:", list(self.data.columns))

        index_column = input(
            "Enter index column name: "
        ).strip()

        value_column = input(
            "Enter values column name: "
        ).strip()

        if index_column not in self.data.columns:
            print("Invalid index column!")
            return

        if value_column not in self.data.columns:
            print("Invalid values column!")
            return

        values = pd.to_numeric(
            self.data[value_column], errors="coerce"
        )

        if values.notna().sum() == 0:
            print("Selected column has no numeric values!")
            return

        temp = self.data.copy()
        temp[value_column] = values

        print("\n1. Sum")
        print("2. Mean")
        print("3. Count")
        print("4. Minimum")
        print("5. Maximum")
        print("6. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "6":
            return

        functions = {
            "1": "sum",
            "2": "mean",
            "3": "count",
            "4": "min",
            "5": "max"
        }

        if choice not in functions:
            print("Invalid choice!")
            return

        try:
            result = pd.pivot_table(
                temp,
                index=index_column,
                values=value_column,
                aggfunc=functions[choice]
            )

            print(result)

        except Exception as e:
            print("Error creating pivot table:", e)

    # 4. Handle Missing Data
    def handle_missing_data(self):
        if not self.check_data():
            return

        while True:
            print("\n== Handle Missing Data ==")
            print("1. Display rows with missing values")
            print("2. Fill missing values with mean")
            print("3. Drop rows with missing values")
            print("4. Replace missing values with a specific value")
            print("5. Back to Main Menu")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                missing_rows = self.data[
                    self.data.isnull().any(axis=1)
                ]

                if missing_rows.empty:
                    print("No missing values found in the dataset!")
                else:
                    print(missing_rows)

            elif choice == "2":
                numeric_columns = self.data.select_dtypes(
                    include=np.number
                ).columns

                if len(numeric_columns) == 0:
                    print("No numeric columns available!")
                else:
                    for column in numeric_columns:
                        mean_value = self.data[column].mean()

                        if pd.notna(mean_value):
                            self.data[column] = (
                                self.data[column].fillna(mean_value)
                            )

                    print("Missing numeric values filled with mean!")

            elif choice == "3":
                before = len(self.data)
                self.data = self.data.dropna().copy()

                print("Rows dropped:", before - len(self.data))

            elif choice == "4":
                value = input(
                    "Enter the value to replace missing values: "
                )

                try:
                    self.data = self.data.fillna(value)
                    print("Missing values replaced successfully!")

                except (ValueError, TypeError) as e:
                    print("Unable to replace values:", e)

            elif choice == "5":
                return

            else:
                print("Invalid choice! Please try again.")

    # 5. Generate Descriptive Statistics
    def generate_statistics(self):
        if not self.check_data():
            return

        print("\n== Descriptive Statistics ==")
        print(self.data.describe(include="all"))

    # 6. Data Visualization
    def visualize_data(self):
        if not self.check_data():
            return

        while True:
            print("\n== Data Visualization ==")
            print("1. Bar Plot")
            print("2. Line Plot")
            print("3. Scatter Plot")
            print("4. Pie Chart")
            print("5. Histogram")
            print("6. Stack Plot")
            print("7. Back to Main Menu")

            choice = input("Enter your choice: ").strip()

            # Back to main menu
            if choice == "7":
                return

            if choice not in ("1", "2", "3", "4", "5", "6"):
                print("Invalid choice! Please try again.")
                continue

            try:
                # Bar Plot, Line Plot and Scatter Plot
                if choice in ("1", "2", "3"):
                    print(
                        "Available columns:",
                        list(self.data.columns)
                    )

                    x = input(
                        "Enter x-axis column name: "
                    ).strip()

                    if x not in self.data.columns:
                        print("Invalid x-axis column!")
                        continue

                    y = input(
                        "Enter y-axis column name: "
                    ).strip()

                    if y not in self.data.columns:
                        print("Invalid y-axis column!")
                        continue

                    plot_data = self.data[[x, y]].copy()

                    # Y-axis must be numeric
                    plot_data[y] = pd.to_numeric(
                        plot_data[y], errors="coerce"
                    )

                    # Line and Scatter require numeric X values
                    if choice in ("2", "3"):
                        plot_data[x] = pd.to_numeric(
                            plot_data[x], errors="coerce"
                        )

                    plot_data = plot_data.dropna(subset=[x, y])

                    if plot_data.empty:
                        print("No valid data available for this plot!")
                        continue

                    fig, ax = plt.subplots(figsize=(8, 5))

                    if choice == "1":
                        # Categorical X values are allowed in Bar Plot
                        bar_data = plot_data.groupby(
                            x, as_index=False, sort=False
                        )[y].sum()

                        ax.bar(
                            bar_data[x].astype(str),
                            bar_data[y]
                        )

                        ax.set_title(f"Bar Plot: {x} vs {y}")
                        ax.set_xlabel(x)
                        ax.set_ylabel(y)

                        plt.setp(
                            ax.get_xticklabels(),
                            rotation=45,
                            ha="right"
                        )

                        plot_name = "Bar plot"

                    elif choice == "2":
                        ax.plot(
                            plot_data[x],
                            plot_data[y],
                            marker="o"
                        )

                        ax.set_title(f"Line Plot: {x} vs {y}")
                        ax.set_xlabel(x)
                        ax.set_ylabel(y)

                        plot_name = "Line plot"

                    else:
                        ax.scatter(
                            plot_data[x],
                            plot_data[y]
                        )

                        ax.set_title(f"Scatter Plot: {x} vs {y}")
                        ax.set_xlabel(x)
                        ax.set_ylabel(y)

                        plot_name = "Scatter plot"

                    fig.tight_layout()
                    self.current_figure = fig
                    plt.show()

                # Pie Chart
                elif choice == "4":
                    print(
                        "Available columns:",
                        list(self.data.columns)
                    )

                    column = input(
                        "Enter column name for pie chart: "
                    ).strip()

                    if column not in self.data.columns:
                        print("Invalid column name!")
                        continue

                    counts = self.data[column].value_counts()

                    if counts.empty:
                        print("No data available!")
                        continue

                    if len(counts) > 10:
                        other = counts.iloc[9:].sum()
                        counts = counts.iloc[:9].copy()
                        counts.loc["Other"] = other

                    fig, ax = plt.subplots(figsize=(8, 5))

                    ax.pie(
                        counts.values,
                        labels=counts.index.astype(str),
                        autopct="%1.1f%%"
                    )

                    ax.set_title(f"Pie Chart: {column}")

                    self.current_figure = fig
                    plt.show()

                    plot_name = "Pie chart"

                # Histogram
                elif choice == "5":
                    column = self.select_numeric_column(
                        "Enter column name for histogram: "
                    )

                    if column is None:
                        continue

                    values = pd.to_numeric(
                        self.data[column], errors="coerce"
                    ).dropna()

                    if values.empty:
                        print("No numeric data available!")
                        continue

                    fig, ax = plt.subplots(figsize=(8, 5))

                    ax.hist(values, bins=10)
                    ax.set_xlabel(column)
                    ax.set_ylabel("Frequency")
                    ax.set_title(f"Histogram: {column}")

                    fig.tight_layout()
                    self.current_figure = fig

                    plt.show()

                    plot_name = "Histogram"

                # Stack Plot
                elif choice == "6":
                    columns = self.data.select_dtypes(
                        include=np.number
                    ).columns.tolist()

                    if not columns:
                        print("No numeric columns available!")
                        continue

                    print("Available numeric columns:", columns)

                    selected = input(
                        "Enter numeric columns separated by commas: "
                    ).strip()

                    selected_columns = [
                        item.strip()
                        for item in selected.split(",")
                        if item.strip()
                    ]

                    if (
                        not selected_columns
                        or any(
                            item not in columns
                            for item in selected_columns
                        )
                    ):
                        print("Invalid column selection!")
                        continue

                    values = self.data[selected_columns].apply(
                        pd.to_numeric, errors="coerce"
                    ).fillna(0)

                    fig, ax = plt.subplots(figsize=(9, 5))

                    ax.stackplot(
                        range(len(values)),
                        *[
                            values[column].to_numpy()
                            for column in selected_columns
                        ],
                        labels=selected_columns
                    )

                    ax.set_xlabel("Row Index")
                    ax.set_ylabel("Values")
                    ax.set_title("Stack Plot")
                    ax.legend(loc="upper left")

                    fig.tight_layout()
                    self.current_figure = fig

                    plt.show()

                    plot_name = "Stack plot"

                print(f"{plot_name} displayed successfully!")

            except Exception as e:
                print("Could not create visualization:", e)

    # 7. Save Visualization
    def save_visualization(self):
        print("\n== Save Visualization ==")

        if self.current_figure is None:
            print("No visualization available to save!")
            return

        filename = input(
            "Enter file name to save the plot "
            "(e.g., scatter_plot.png): "
        ).strip()

        if not filename:
            filename = "visualization.png"

        if not filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".pdf", ".svg")
        ):
            filename += ".png"

        try:
            self.current_figure.savefig(
                filename,
                dpi=300,
                bbox_inches="tight"
            )

            print(
                f"Visualization saved as {filename} successfully!"
            )

        except Exception as e:
            print("Error saving visualization:", e)

    # Main Menu
    def run(self):
        while True:
            print(
                "\n========== Data Analysis & Visualization Program =========="
            )
            print("Please select an option:")
            print("1. Load Dataset")
            print("2. Explore Data")
            print("3. Perform DataFrame Operations")
            print("4. Handle Missing Data")
            print("5. Generate Descriptive Statistics")
            print("6. Data Visualization")
            print("7. Save Visualization")
            print("8. Exit")
            print(
                "============================================================"
            )

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.load_data()

            elif choice == "2":
                self.explore_data()

            elif choice == "3":
                self.dataframe_operations()

            elif choice == "4":
                self.handle_missing_data()

            elif choice == "5":
                self.generate_statistics()

            elif choice == "6":
                self.visualize_data()

            elif choice == "7":
                self.save_visualization()

            elif choice == "8":
                print("Exiting the program. Goodbye!")
                break

            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    analyzer = SalesDataAnalyzer()

    try:
        analyzer.run()

    except KeyboardInterrupt:
        print("\nExiting the program. Goodbye!")

    finally:
        if analyzer.current_figure is not None:
            plt.close(analyzer.current_figure)