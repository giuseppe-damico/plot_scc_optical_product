import matplotlib.pyplot as plt
import numpy as np


def set_profile_color_type(wave, profile_type):
    wave_int = int(wave)

    # Normalize profile_type to avoid case issues
    profile_type = profile_type.lower()

    # Color definitions
    if profile_type == "elda":
        colors = {
            1064: "#ff0000",
            532: "#00aa00",
        }
        default_color = "#0066ff"
    elif profile_type == "eldamwl":
        # darker variants
        colors = {
            1064: "darkred",
            532: "darkgreen",
        }
        default_color = "darkblue"
    else:
        raise ValueError(f"Unknown profile_type: {profile_type}")

    return colors.get(wave_int, default_color)


def make_plots(ew, ee, filename=None):
    # Generate plot
    n_raw = 2
    n_col = 3
    fig, ax = plt.subplots(n_raw, n_col, figsize=(16,10), squeeze=False, sharey=True)

    fig.tight_layout(rect=[0, 0, 1, 0.95], pad=1.5, h_pad=1.5, w_pad=1.2)

    unique_measids = sorted(list(set(obj._ga_measurement_ID for obj in ee)))
    # Join using ";" as separator
    mid = ";".join(unique_measids)
    title = "ELDAmwl (" + ew._ga_measurement_ID + ") ELDA ("+mid+")"
    fig.suptitle(title, y=0.98)

    # Low resolution backscatter plot
    to_be_plot=0
    if ew._gr_lowres_products._va_backscatter.size > 0:
        to_be_plot=1
        n_wave, n_time, n_point=ew._gr_lowres_products._va_backscatter.shape
        for t in range(n_time):
            lss="-"
            y = ew._gr_lowres_products._va_altitude[t, :]*0.001
            for w in range(n_wave):
                wave=ew._gr_lowres_products._va_wavelength[w]
                x=ew._gr_lowres_products._va_backscatter[w,t,:]*1e6
                x_err=ew._gr_lowres_products._va_error_backscatter[w,t,:]*1e6
                if n_time == 1:
                    label_txt = "ELDAmwl-"+ str(wave)
                else:
                    label_txt="ELDAmwl-"+str(wave)+ " t=" + str(t)
                ax[0,0].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'eldamwl'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)

    for i in range(len(ee)):
        if ee[i]._va_extinction.size>0 and ee[i]._va_backscatter.size>0:
            to_be_plot=1
            n_wave, n_time, n_point = ee[i]._va_backscatter.shape
            y = ee[i]._va_altitude[:] * 0.001
            for t in range(n_time):
                lss = "--"
                for w in range(n_wave):
                    wave = ee[i]._va_wavelength[w]
                    x = ee[i]._va_backscatter[w, t, :] * 1e6
                    x_err = ee[i]._va_error_backscatter[w, t, :] * 1e6
                    if n_time == 1:
                        label_txt = "ELDA-"+ str(wave)
                    else:
                        label_txt = "ELDA-"+ str(wave) + " t=" + str(t)
                    ax[0,0].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'elda'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)
    if to_be_plot == 1:
        ax[0, 0].set_ylabel("Height [km]")
        ax[0, 0].set_xlabel("Backscatter [Mm$^{-1}$sr$^{-1}$]")
        ax[0, 0].legend(fontsize="small")
        ax[0, 0].grid(True)
    else:
        ax[0,0].axis("off")

    # Low resolution depolarization plot
    to_be_plot=0
    if ew._gr_lowres_products._va_volumedepolarization.size > 0:
        to_be_plot=1
        n_wave, n_time, n_point=ew._gr_lowres_products._va_volumedepolarization.shape
        for t in range(n_time):
            lss="-"
            y = ew._gr_lowres_products._va_altitude[t, :]*0.001
            for w in range(n_wave):
                wave=ew._gr_lowres_products._va_wavelength[w]
                x=ew._gr_lowres_products._va_volumedepolarization[w,t,:]
                x_err=ew._gr_lowres_products._va_error_volumedepolarization[w,t,:]
                if n_time == 1:
                    label_txt = "ELDAmwl-"+ str(wave)
                else:
                    label_txt="ELDAmwl-"+str(wave)+ " t=" + str(t)
                ax[0,1].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'eldamwl'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)

    for i in range(len(ee)):
        if ee[i]._va_volumedepolarization.size>0:
            to_be_plot=1
            n_wave, n_time, n_point = ee[i]._va_volumedepolarization.shape
            y = ee[i]._va_altitude[:] * 0.001
            for t in range(n_time):
                lss = "--"
                for w in range(n_wave):
                    wave = ee[i]._va_wavelength[w]
                    x = ee[i]._va_volumedepolarization[w, t, :]
                    x_err = ee[i]._va_error_volumedepolarization[w, t, :]
                    if n_time == 1:
                        label_txt = "ELDA-"+ str(wave)
                    else:
                        label_txt = "ELDA-"+ str(wave) + " t=" + str(t)
                    ax[0,1].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'elda'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)
    if to_be_plot == 1:
        ax[0, 1].set_ylabel("Height [km]")
        ax[0, 1].set_xlabel("Depolarization")
        ax[0, 1].legend(fontsize="small")
        ax[0, 1].grid(True)
    else:
        ax[0,1].axis("off")

    # Low resolution extinction plot
    to_be_plot=0
    if ew._gr_lowres_products._va_extinction.size > 0:
        to_be_plot=1
        n_wave, n_time, n_point=ew._gr_lowres_products._va_extinction.shape
        for t in range(n_time):
            lss="-"
            y = ew._gr_lowres_products._va_altitude[t, :]*0.001
            for w in range(n_wave):
                wave=ew._gr_lowres_products._va_wavelength[w]
                x=ew._gr_lowres_products._va_extinction[w,t,:]*1e6
                x_err=ew._gr_lowres_products._va_error_extinction[w,t,:]*1e6
                if n_time == 1:
                    label_txt = "ELDAmwl-"+ str(wave)
                else:
                    label_txt="ELDAmwl-"+str(wave)+ " t=" + str(t)
                ax[0,2].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'eldamwl'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)

    # Limit negative values of extinction shown (symmetric x-axis limits or -50 as lowest)
    x_all_max = 0
    # ELDAmwl
    ext_data = ew._gr_lowres_products._va_extinction
    if ext_data.size > 0:
        x_all_max = max(x_all_max, np.nanmax(np.abs(ext_data * 1e6)))
    # ELDA
    for i in range(len(ee)):
        ext_data = ee[i]._va_extinction
        if ext_data.size > 0:
            x_all_max = max(x_all_max, np.nanmax(np.abs(ext_data * 1e6)))
    # Apply limits only if valid data exists
    if x_all_max > 0:
        xmin = -1.1 * x_all_max
        xmax = 1.1 * x_all_max
        # lower limit to -50
        if xmin < -50:
            xmin = -50
        ax[0, 2].set_xlim(xmin, xmax)

    for i in range(len(ee)):
        if ee[i]._va_extinction.size>0:
            to_be_plot=1
            n_wave, n_time, n_point = ee[i]._va_extinction.shape
            y = ee[i]._va_altitude[:] * 0.001
            for t in range(n_time):
                lss = "--"
                for w in range(n_wave):
                    wave = ee[i]._va_wavelength[w]
                    x = ee[i]._va_extinction[w, t, :]*1e6
                    x_err = ee[i]._va_error_extinction[w, t, :]*1e6
                    if n_time == 1:
                        label_txt = "ELDA-"+ str(wave)
                    else:
                        label_txt = "ELDA-"+ str(wave) + " t=" + str(t)
                    ax[0,2].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'elda'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)
    if to_be_plot == 1:
        ax[0, 2].set_ylabel("Height [km]")
        ax[0, 2].set_xlabel("Extinction [Mm$^{-1}$]")
        ax[0, 2].legend(fontsize="small")
        ax[0, 2].grid(True)
    else:
        ax[0,2].axis("off")

    # High resolution backscatter plot
    to_be_plot=0
    if ew._gr_highres_products._va_backscatter.size > 0:
        to_be_plot=1
        n_wave, n_time, n_point=ew._gr_highres_products._va_backscatter.shape
        for t in range(n_time):
            lss="-"
            y = ew._gr_highres_products._va_altitude[t, :]*0.001
            for w in range(n_wave):
                wave=ew._gr_highres_products._va_wavelength[w]
                x=ew._gr_highres_products._va_backscatter[w,t,:]*1e6
                x_err=ew._gr_highres_products._va_error_backscatter[w,t,:]*1e6
                if n_time == 1:
                    label_txt = "ELDAmwl-"+ str(wave)
                else:
                    label_txt="ELDAmwl-"+str(wave)+ " t=" + str(t)
                ax[1,0].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'eldamwl'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)

    for i in range(len(ee)):
        if ee[i]._va_extinction.size==0 and ee[i]._va_backscatter.size>0:
            to_be_plot=1
            n_wave, n_time, n_point = ee[i]._va_backscatter.shape
            y = ee[i]._va_altitude[:] * 0.001
            for t in range(n_time):
                lss = "--"
                for w in range(n_wave):
                    wave = ee[i]._va_wavelength[w]
                    x = ee[i]._va_backscatter[w, t, :] * 1e6
                    x_err = ee[i]._va_error_backscatter[w, t, :] * 1e6
                    if n_time == 1:
                        label_txt = "ELDA-"+ str(wave)
                    else:
                        label_txt = "ELDA-"+ str(wave) + " t=" + str(t)
                    ax[1,0].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'elda'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)
    if to_be_plot == 1:
        ax[1, 0].set_ylabel("Height [km]")
        ax[1, 0].set_xlabel("Backscatter [Mm$^{-1}$sr$^{-1}$]")
        ax[1, 0].legend(fontsize="small")
        ax[1, 0].grid(True)
    else:
        ax[1,0].axis("off")

    # High resolution depolarization plot
    to_be_plot=0
    if ew._gr_highres_products._va_volumedepolarization.size > 0:
        to_be_plot=1
        n_wave, n_time, n_point=ew._gr_highres_products._va_volumedepolarization.shape
        for t in range(n_time):
            lss="-"
            y = ew._gr_highres_products._va_altitude[t, :]*0.001
            for w in range(n_wave):
                wave=ew._gr_highres_products._va_wavelength[w]
                x=ew._gr_highres_products._va_volumedepolarization[w,t,:]
                x_err=ew._gr_highres_products._va_error_volumedepolarization[w,t,:]
                if n_time == 1:
                    label_txt = "ELDAmwl-"+ str(wave)
                else:
                    label_txt="ELDAmwl-"+str(wave)+ " t=" + str(t)
                ax[1,1].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'eldamwl'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)

    for i in range(len(ee)):
        if ee[i]._va_volumedepolarization.size>0:
            to_be_plot=1
            n_wave, n_time, n_point = ee[i]._va_volumedepolarization.shape
            y = ee[i]._va_altitude[:] * 0.001
            for t in range(n_time):
                lss = "--"
                for w in range(n_wave):
                    wave = ee[i]._va_wavelength[w]
                    x = ee[i]._va_volumedepolarization[w, t, :]
                    x_err = ee[i]._va_error_volumedepolarization[w, t, :]
                    if n_time == 1:
                        label_txt = "ELDA-"+ str(wave)
                    else:
                        label_txt = "ELDA-"+ str(wave) + " t=" + str(t)
                    ax[1,1].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'elda'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)
    if to_be_plot == 1:
        ax[1, 1].set_ylabel("Height [km]")
        ax[1, 1].set_xlabel("Depolarization")
        ax[1, 1].legend(fontsize="small")
        ax[1, 1].grid(True)
    else:
        ax[1,1].axis("off")

    # High resolution extinction plot
    to_be_plot=0
    if ew._gr_highres_products._va_extinction.size > 0:
        to_be_plot=1
        n_wave, n_time, n_point=ew._gr_highres_products._va_extinction.shape
        for t in range(n_time):
            lss="-"
            y = ew._gr_highres_products._va_altitude[t, :]*0.001
            for w in range(n_wave):
                wave=ew._gr_highres_products._va_wavelength[w]
                x=ew._gr_highres_products._va_extinction[w,t,:]*1e6
                x_err=ew._gr_highres_products._va_error_extinction[w,t,:]*1e6
                if n_time == 1:
                    label_txt = "ELDAmwl-"+ str(wave)
                else:
                    label_txt="ELDAmwl-"+str(wave)+ " t=" + str(t)
                ax[1,2].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'eldamwl'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)

    # Limit negative values of extinction shown (symmetric x-axis limits, minimum -50)
    x_all_max = 0
    # ELDAmwl
    ext_data = ew._gr_highres_products._va_extinction
    if ext_data.size > 0:
        x_all_max = max(x_all_max, np.nanmax(np.abs(ext_data * 1e6)))
    # ELDA
    for i in range(len(ee)):
        ext_data = ee[i]._va_extinction
        if ext_data.size > 0:
            x_all_max = max(x_all_max, np.nanmax(np.abs(ext_data * 1e6)))
    # Apply limits only if valid data exists
    if x_all_max > 0:
        xmin = -1.1 * x_all_max
        xmax = 1.1 * x_all_max
        # lower limit to -50
        if xmin < -50:
            xmin = -50
        ax[1, 2].set_xlim(xmin, xmax)

    for i in range(len(ee)):
        if ee[i]._va_extinction.size>0:
            to_be_plot=1
            n_wave, n_time, n_point = ee[i]._va_extinction.shape
            y = ee[i]._va_altitude[:] * 0.001
            for t in range(n_time):
                lss = "--"
                for w in range(n_wave):
                    wave = ee[i]._va_wavelength[w]
                    x = ee[i]._va_extinction[w, t, :]*1e6
                    x_err = ee[i]._va_error_extinction[w, t, :]*1e6
                    if n_time == 1:
                        label_txt = "ELDA-"+ str(wave)
                    else:
                        label_txt = "ELDA-"+ str(wave) + " t=" + str(t)
                    ax[1,2].errorbar(x, y, xerr=x_err, color=set_profile_color_type(wave, 'elda'), ls=lss, label=label_txt,
                                 alpha=0.6, elinewidth=0.7, capsize=0, linewidth=2)
    if to_be_plot == 1:
        ax[1, 2].set_ylabel("Height [km]")
        ax[1, 2].set_xlabel("Extinction [Mm$^{-1}$]")
        ax[1, 2].legend(fontsize="small")
        ax[1, 2].grid(True)
    else:
        ax[1,2].axis("off")

    for i in range(n_raw):
        for j in range(n_col):
            ax[i, j].tick_params(labelleft=True)

    if filename:
        plt.rcParams.update({
            'font.size': 8,
            'axes.labelsize': 9,
            'xtick.labelsize': 7,
            'ytick.labelsize': 7,
            'legend.fontsize': 7
        })

        fig.tight_layout(pad=0.8, h_pad=0.5, w_pad=0.5)

        plt.savefig(
            filename,
            dpi=300,
            bbox_inches='tight',
            transparent=False
        )
    else:
        plt.tight_layout()
        plt.show()