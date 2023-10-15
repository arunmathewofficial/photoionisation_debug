import os
import numpy as np
import matplotlib.pyplot as plt  # importing matplotlib package
from ReadTable import ReadTable_Advance

chianti_dir = "/home/tony/Desktop/pion/photoionisation_test/MPV10-LUTs/cooling-tables/chianti/"
mellema_dir = "/home/tony/Desktop/pion/photoionisation_test/MPV10-LUTs/cooling-tables/mellema/"

Output_dir = "/home/tony/Desktop/pion/photoionisation_test/cooling_tables/"

chianti_list = os.listdir(chianti_dir)

# Filter and print only files with a ".txt" extension.
for chianti_file in chianti_list:

    if chianti_file.endswith(".txt"):
        parts = chianti_file.split(".")
        parts = chianti_file.split('_')
        if len(parts) > 1:
            species = parts[-1].split('.')[0]
        else:
            print("Underscore not found in the filename.")

        # make both mellema_file and chianti file
    mellema_file = mellema_dir + "mellema_rates_" + species + ".txt"
    chianti_file = chianti_dir + chianti_file

    ##############################################################################################
    chinati_tab = ReadTable_Advance(chianti_file)
    print("Table Size: ( row =", chinati_tab['N_row'], ", columns = ", chinati_tab['N_col'], ")")
    N_col = chinati_tab['N_col']

    Chianti_ne = np.linspace(1.0, 6.0, N_col)
    Chianti_Temperature = chinati_tab['Temperature']
    Chianti_Data = chinati_tab['columns']

    # make the rate table
    N_row = chinati_tab['N_row']
    # Create T_row arrays
    Chianti_LUT_Rate = [[] for _ in range(N_row)]
    # Append corresponding data into each row
    for r in range(N_row):
        # excluding column 1
        for c in range(0, chinati_tab['N_col']):
            Chianti_LUT_Rate[r].append(Chianti_Data[c][r])

    # create 2d x,y grid for LUT generated data
    Chianti_LUT_X, Chianti_LUT_Y = np.meshgrid(Chianti_ne, Chianti_Temperature)
    Chianti_LUT_Rate = np.array(Chianti_LUT_Rate)
    ##############################################################################################

    ##############################################################################################
    mellema_tab = ReadTable_Advance(mellema_file)
    print("Table Size: ( row =", mellema_tab['N_row'], ", columns = ", mellema_tab['N_col'], ")")
    N_col = mellema_tab['N_col']

    Mellema_ne = np.linspace(1.0, 6.0, N_col)
    Mellema_Temperature = mellema_tab['Temperature']
    Mellema_Data = mellema_tab['columns']

    # make the rate table
    N_row = mellema_tab['N_row']
    # Create T_row arrays
    Mellema_LUT_Rate = [[] for _ in range(N_row)]
    # Append corresponding data into each row
    for r in range(N_row):
        # excluding column 1
        for c in range(0, mellema_tab['N_col']):
            Mellema_LUT_Rate[r].append(Mellema_Data[c][r])

    # create 2d x,y grid for LUT generated data
    Mellema_LUT_X, Mellema_LUT_Y = np.meshgrid(Mellema_ne, Mellema_Temperature)
    Mellema_LUT_Rate = np.array(Mellema_LUT_Rate)
    ##############################################################################################

    print("Plotting Chianti & Mellema cooling rate table:" + species)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plt.title(species)
    ax.plot_surface(Chianti_LUT_X, Chianti_LUT_Y, Chianti_LUT_Rate, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none', label="Chianti")
    ax.plot_surface(Mellema_LUT_X, Mellema_LUT_Y, Mellema_LUT_Rate, rstride=1, cstride=1, cmap='cool', edgecolor='none', label="Mellema")
    #ax.scatter3D(Mellema_LUT_X, Mellema_LUT_Y, Mellema_LUT_Rate, label='Mellema', color='red')
    ax.set_xlabel('Log_ne')
    ax.set_ylabel('Log_T')
    ax.set_zlabel('Rate')
    # Set the view to face the x-axis
    ax.view_init(elev=0, azim=0)  # Adjust the angles as needed
    #plt.show(block=True)
    #ax.legend()
    image_name = Output_dir + species + '.png'
    print("Saving " + image_name)
    fig.savefig(image_name)
    plt.close(fig)










