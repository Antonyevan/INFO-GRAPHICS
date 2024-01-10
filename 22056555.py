# -*- coding: utf-8 -*-
"""
Created on Tue Jan 9 02:27:48 2024

@author: aa23aan
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import textwrap

def read_data(file_path):
    """
    Read data from the CSV file.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - pd.DataFrame: DataFrame containing the read data.
    """
    return pd.read_csv(file_path)

def filter_data(df, selected_countries, start_year, end_year):
    """
    Filter data based on selected countries and a specific time range.

    Parameters:
    - df (pd.DataFrame): Input DataFrame.
    - selected_countries (list): List of countries to filter.
    - start_year (int): Start year of the time range.
    - end_year (int): End year of the time range.

    Returns:
    - pd.DataFrame: Filtered DataFrame.
    """
    df_selected = df[df['country'].isin(selected_countries)]
    return df_selected[(df_selected['year'] >= start_year) & (df_selected['year'] <= end_year)]

def plot_wind_energy_trend(df_selected, selected_countries):
    """
    Plot the trend of wind energy production over time.

    Parameters:
    - df_selected (pd.DataFrame): Filtered DataFrame.
    - selected_countries (list): List of countries.

    Returns:
    - None
    """
    plt.figure(figsize=(8, 6))
    for country in selected_countries:
        df_country = df_selected[df_selected['country'] == country]
        plt.plot(df_country['year'], df_country['wind_electricity'], marker='o', label=country)

    plt.title('Electricity Generation from Wind (2012-2022)',color='#8B4513',weight='bold')
    plt.xlabel('Year')
    plt.ylabel('Renewable Energy Consumption (TWh)')
    plt.legend()
    plt.savefig('Wind_energy_plot.png', dpi=300)

def plot_electricity_generation_mix(df_selected, selected_countries):
    """
    Plot the electricity generation mix using a stacked bar chart.

    Parameters:
    - df_selected (pd.DataFrame): Filtered DataFrame.
    - selected_countries (list): List of countries.

    Returns:
    - None
    """
    df_2018 = df_selected[df_selected['year'] == 2022]
    plt.figure(figsize=(8, 6))
    sns.set_palette("deep", n_colors=len(df_selected['country'].unique()))
    energy_types = ['greenhouse_gas_emissions','coal_electricity','fossil_electricity']

    bar_width = 0.2
    for i, energy_type in enumerate(energy_types):
        x_coordinates = [j + i * bar_width for j in range(len(selected_countries))]
        plt.bar(x_coordinates, df_2018[energy_type], width=bar_width, \
                label=f'{energy_type.replace("_", " ").title()}', alpha=0.7)

    plt.xticks([j + bar_width for j in range(len(selected_countries))], selected_countries)
    plt.title('Green House Gas Emission vs Carbon and fossil electricity production (2022)'\
              ,color='#8B4513',weight='bold')
    plt.xlabel('Country')
    plt.ylabel('Electricity Generation (TWh)')
    plt.legend(title='Energy Type')
    plt.savefig('electricity_generation_mix_plot.png', dpi=300)

def plot_carbon_intensity(df_selected, selected_countries):
    """
    Plot the carbon intensity of electricity generation over time.

    Parameters:
    - df_selected (pd.DataFrame): Filtered DataFrame.
    - selected_countries (list): List of countries.

    Returns:
    - None
    """
    plt.figure(figsize=(8, 6))
    for country in selected_countries:
        df_country = df_selected[df_selected['country'] == country]
        plt.plot(df_country['year'], df_country['carbon_intensity_elec'], marker='o', label=country)

    plt.title('Carbon Intensity of Electricity Generation Over Time (2012-2022)',color='#8B4513',weight='bold')
    plt.xlabel('Year')
    plt.ylabel('Carbon Intensity (gCO2/kWh)')
    plt.legend()
    plt.savefig('carbon_intensity_plot.png', dpi=300)

def plot_china_electricity_production_pie(df_energy):
    """
    Plot a pie chart for China's electricity production sources in 2022.

    Parameters:
    - df_energy (pd.DataFrame): Input DataFrame.

    Returns:
    - None
    """
    china_data_2018 = df_energy[(df_energy['country'] == 'China') & (df_energy['year'] == 2022)]
    labels = ['Coal', 'Gas', 'Nuclear', 'Hydro', 'Wind', 'Solar', 'Fossil', 'Bio']
    sizes = china_data_2018[['coal_electricity', 'gas_electricity', 'nuclear_electricity',
                              'hydro_electricity', 'wind_electricity', 'solar_electricity',
                              'fossil_electricity', 'biofuel_electricity']].iloc[0]

    explode = (0.02, 0.02, 0.02, 0.02, 0.25, 0.02, 0.02, 0.02)

    fig, ax = plt.subplots(figsize=(8, 6))
    pie, _, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                               colors = ['#FF9999', '#FFD699', '#FFEB99', \
                                         '#CCFFCC', '#3366CC', '#CC99FF', '#FFCCE5', '#FFD9B3'],
                               explode=explode, pctdistance=0.85, wedgeprops=dict(edgecolor='grey'))

    fig.set_size_inches(8, 6)

    for i, autotext in enumerate(autotexts):
        autotext.set_bbox(dict(boxstyle='round,pad=0.3', edgecolor='white', facecolor='white'))

    plt.title("China's Electricity Production from Different Sources in 2022",color='#8B4513',weight='bold')
    plt.savefig('china_electricity_production_pie.png', dpi=300)

def paste_with_rounded_corners_and_gap(combined_img, image_path, position, size, corner_radius, gap):
    """
    Paste an image onto a combined image with rounded corners and a gap.

    Parameters:
    - combined_img (PIL.Image.Image): Combined image.
    - image_path (str): Path to the image to be pasted.
    - position (tuple): Position where the image will be pasted.
    - size (tuple): Size of the pasted image.
    - corner_radius (int): Radius of the rounded corners.
    - gap (int): Gap between images.

    Returns:
    - None
    """
    img = Image.open(image_path)
    img = img.convert("RGBA")
    img = img.resize(size)
    mask = Image.new("L", img.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([(0, 0), img.size], corner_radius, fill=255)
    img.putalpha(mask)
    combined_img.paste(img, (position[0], position[1] + gap), img)


def create_combined_image(df_selected, selected_countries, df_energy, paragraphs):
    """
    Create a combined image with various visualizations and findings.

    Parameters:
    - df_selected (pd.DataFrame): Filtered DataFrame.
    - selected_countries (list): List of countries.
    - df_energy (pd.DataFrame): Input DataFrame.
    - paragraphs (list): List of paragraphs to be displayed in separate text boxes.

    Returns:
    - None
    """
    combined_img = Image.new('RGB', (2400, 1500), color='#B0C4DE')
    draw = ImageDraw.Draw(combined_img)

    heading = "Global Influence: China and India's Power Impact"
    heading_font = ImageFont.truetype("arial.ttf", 50)
    heading_width, heading_height = draw.textsize(heading, font=heading_font)
    heading_position = ((combined_img.width - heading_width) // 2, 30)
    draw.text(heading_position, heading, font=heading_font, fill='#333333')

    description = "This infographic illustrates China's Wind Energy Triumph and Global Electricity Dynamics"
    description_font = ImageFont.truetype("arial.ttf", 30)
    description_width, description_height = draw.textsize(description, font=description_font)
    description_position = ((combined_img.width - description_width) // 2, heading_height + 50)
    draw.text(description_position, description, font=description_font, fill='#555555')

    # Calculate available space on both sides
    left_space = 50
    right_space = combined_img.width - 850  # 50 (left space) + 800 (wind energy graph width)
    graph_width = 800
    gap = 20

    # Calculate position for the wind energy graph
    wind_energy_position = (left_space, heading_height + 150)
    paste_with_rounded_corners_and_gap(combined_img, 'Wind_energy_plot.png',
                                       wind_energy_position, (graph_width, 600), 40, gap)

    # Calculate position for the pie chart
    pie_chart_position = (left_space, heading_height + 150 + 600 + gap)
    paste_with_rounded_corners_and_gap\
        (combined_img, 'china_electricity_production_pie.png',
                                       pie_chart_position, (graph_width, 600), 40, gap)

    # Calculate position for the carbon intensity graph
    carbon_intensity_position = (right_space, heading_height + 150)
    paste_with_rounded_corners_and_gap\
        (combined_img, 'carbon_intensity_plot.png',
                                       carbon_intensity_position, (graph_width, 600), 40, gap)

    # Calculate position for the electricity generation mix graph
    electricity_generation_mix_position = (right_space, heading_height + 150 + 600 + gap)
    paste_with_rounded_corners_and_gap(combined_img, 'electricity_generation_mix_plot.png',
                                       electricity_generation_mix_position, (graph_width, 600), 40, gap)

    # Calculate position for the text boxes
    textbox_width = 650
    textbox_gap = 20
    textbox_position_y = heading_height + 150

    for i, paragraph in enumerate(paragraphs):
        # Calculate the required height for the current paragraph
        font_path = 'times.ttf'  # Provide the correct path to your times.ttf file
        textbox_font = ImageFont.truetype(font_path, 30)
        wrapped_text = textwrap.fill(paragraph, width=41)
        _, wrapped_text_height = draw.textsize(wrapped_text, font=textbox_font)

        textbox_position = ((combined_img.width - textbox_width) // 2, textbox_position_y)
        textbox_height = wrapped_text_height + 40  # Add some padding

        draw.rectangle([textbox_position, \
                        (textbox_position[0] + textbox_width, textbox_position[1] + textbox_height)],
                       fill='#FFFFFF')

        # Draw the wrapped text inside the textbox with automatic wrapping
        draw.multiline_text((textbox_position[0] + \
                             20, textbox_position[1] + 20), wrapped_text, \
                            font=textbox_font, fill='#000000', align="left")

        textbox_position_y += textbox_height + textbox_gap

    combined_img.save('22056555.png', dpi=(300, 300))

# Main execution
file_path = 'World Energy Consumption.csv'
df_energy = read_data(file_path)

selected_countries = ['Canada', 'India', 'China', 'Japan', 'United Kingdom']
df_selected = filter_data(df_energy, selected_countries, 2012, 2022)

plot_wind_energy_trend(df_selected, selected_countries)
plot_electricity_generation_mix(df_selected, selected_countries)
plot_carbon_intensity(df_selected, selected_countries)
plot_china_electricity_production_pie(df_energy)

paragraphs = [
    "Wind Leadership (2012-2022): From 2012 to 2022, China emerged as a leader in wind electricity production, a commendable move towards cleaner energy.",
    "Electricity Mix Snapshot (2022): However, in 2022, only 5.5% of China's electricity came from wind, with coal and fossil fuels dominating, as depicted in the Electricity Production Pie graph.",
    "Global Impact Dynamics: The global impact of China and India in electricity generation brings both praise and challenges, as pollution accompanies their significant roles. This insight is discerned from the Green House Gas Emission vs Carbon and fossil electricity production graph.",
    "India-China Dynamics: India outshines China in fossil and coal electricity production, as seen in the Electricity Generation Mix and Carbon Intensity graphs. Meanwhile, China grapples with high greenhouse gas emissions, evident in the Carbon Intensity graph.",
    "Energy Exploration and Competition: We explore wind energy growth, China's energy choices, global challenges, and India-China competition in fossil electricity. These insights, in the graphs, stress the balance for progress and environmental stewardship."
]

#Calls function to save output image
create_combined_image(df_selected, selected_countries, df_energy, paragraphs)