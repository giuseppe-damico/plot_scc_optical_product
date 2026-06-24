import matplotlib.pyplot as plt
from eldamwl import Eldamwl, set_profile_color
from elda import Elda

def make_plots(ew, ee):
    # Generate plot
    n_raw = 2
    n_col = 3
    fig, ax = plt.subplots(n_raw, n_col, squeeze=False)
    title = "ELDAmwl (" + ew._ga_measurement_ID + ") ELDA ("
    for i in range(len(ee)):
        title += ee[i]._ga_measurement_ID + " "
    title += ")"
    fig.suptitle(title)

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
                ax[0,0].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt )

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
                    ax[0,0].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
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
                ax[0,1].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt )

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
                    ax[0,1].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
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
                ax[0,2].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt )

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
                    ax[0,2].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
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
                ax[1,0].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt )

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
                    ax[1,0].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
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
                ax[1,1].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt )

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
                    ax[1,1].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
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
                ax[1,2].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt )

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
                    ax[1,2].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
    if to_be_plot == 1:
        ax[1, 2].set_ylabel("Height [km]")
        ax[1, 2].set_xlabel("Extinction [Mm$^{-1}$]")
        ax[1, 2].legend(fontsize="small")
        ax[1, 2].grid(True)
    else:
        ax[1,2].axis("off")

    #fig.text(
    #    0.5,
    #    0.02,
    #    "Filename: " + ew.filename,
    #    ha="center",
    #    va="bottom",
    #    fontsize=8
    #)
    plt.tight_layout(pad=0.3, h_pad=0.1, w_pad=0.1)
    plt.show()