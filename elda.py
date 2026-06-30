import sys
from dataclasses import dataclass, field, fields
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
import os

def set_profile_color(wave):
    wave_int = int(wave)
    if wave_int == 1064:
        color = 'red'
    elif wave_int == 532:
        color = 'green'
    else:
        color = 'blue'
    return color

@dataclass
class Elda:
    filename: str= ""
    _ga_measurement_ID: str = ""
    _ga_system: str = ""
    _ga_institution: str = ""
    _ga_location: str = ""
    _ga_station_ID: str = ""
    _ga_PI: str = ""
    _ga_PI_affiliation: str = ""
    _ga_PI_affiliation_acronym: str = ""
    _ga_PI_address: str = ""
    _ga_PI_phone: str = ""
    _ga_PI_email: str = ""
    _ga_Data_Originator: str = ""
    _ga_Data_Originator_affiliation: str = ""
    _ga_Data_Originator_affiliation_acronym: str = ""
    _ga_Data_Originator_address: str = ""
    _ga_Data_Originator_phone: str = ""
    _ga_Data_Originator_email: str = ""
    _ga_data_processing_institution: str = ""
    _ga_comment: str = ""
    _ga_scc_version: str = ""
    _ga_scc_version_description: str = ""
    _ga_processor_name: str = ""
    _ga_processor_version: str = ""
    _ga_history: str = ""
    _ga_title: str = ""
    _ga_source: str = ""
    _ga_references: str = ""
    _ga___file_format_version: str = ""
    _ga_Conventions: str = ""
    _ga_hoi_system_ID: int = 0
    _ga_hoi_configuration_ID: int = 0
    _ga_input_file: str = ""
    _ga_measurement_start_datetime: str = ""
    _ga_measurement_stop_datetime: str = ""

    _va_altitude: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_time: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_time_bounds: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_vertical_resolution: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    _va_cloud_mask: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_cirrus_contamination: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_cloud_mask_type: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_cirrus_contamination_source: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    _va_error_retrieval_method: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_scc_product_type: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_user_defined_category: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    _va_backscatter_evaluation_method: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_raman_backscatter_algorithm: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_backscatter: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_backscatter: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_backscatter_calibration_value: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_backscatter_calibration_search_range: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_backscatter_calibration_range_search_algorithm: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_backscatter_calibration_range: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_elastic_backscatter_algorithm: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_assumed_particle_lidar_ratio: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    _va_molecular_calculation_source: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_latitude: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_longitude: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_station_altitude: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    _va_wavelength: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_zenith_angle: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_shots: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_earlinet_product_type: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    _va_volumedepolarization: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_volumedepolarization: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_particledepolarization: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_particledepolarization: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    _va_extinction_evaluation_algorithm: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_extinction: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_extinction: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_extinction_assumed_wavelength_dependence: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    def from_netcdf(self,file_name):
        self.filename = os.path.basename(file_name)
        try:
            with nc.Dataset(file_name, 'r') as ds:
                for f in fields(self):
                    # Getting global attributes
                    # Getting all the dataclass members whose name starts with "_ga_"
                    if f.name.startswith("_ga_"):
                        member_name = f.name
                        member_type = f.type
                        attribute_name=member_name.replace("_ga_", "")
                        if attribute_name in ds.ncattrs():
                            # Read the attribute value
                            setattr(self, member_name, member_type(ds.getncattr(attribute_name)))
                        else:
                            print(f"Attribute '{attribute_name}' not found in the NetCDF file {file_name}.")

                    # Getting variables
                    # Getting all the dataclass members whose name starts with "_va_"
                    elif f.name.startswith("_va_"):
                        member_name = f.name
                        #member_type = f.type
                        variable_name = member_name.replace("_va_", "")
                        #print("VARIABLE: ", variable_name)
                        is_variable_present = False
                        for var_name, var in ds.variables.items():
                            if var_name == variable_name:
                                is_variable_present=True
                                fill_value = getattr(var, "_FillValue", None)
                                buffer=var[:]
                                if fill_value is not None:
                                    buffer = np.ma.masked_equal(buffer, fill_value)
                                setattr(self, member_name, buffer)
                        if not is_variable_present:
                            print(f"Variable '{variable_name}' not found in the NetCDF file {file_name}.")
        except FileNotFoundError:
            print(f"The file '{file_name}' does not exist!")
            sys.exit(1)
        except OSError as e:
            print(f"Error in reading NetCDF file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unknown error in reading NetCDF file: {e}")
            sys.exit(1)

    def plot(self):
        is_ext_included = 0
        is_dep_included = 0
        is_bck_included = 0
        if self._va_backscatter.size >0:
            is_bck_included=1
        if self._va_extinction.size > 0:
            is_ext_included = 1
        if self._va_volumedepolarization.size > 0:
            is_dep_included = 1
        n_raw=1
        #n_col=is_bck_included+is_ext_included+is_dep_included
        n_col=3
        # Creating the needed subplots
        fig, ax = plt.subplots(n_raw, n_col, squeeze=False)
        title="ELDA: "+self._ga_measurement_ID +" ("+self._ga_system +", "+self._ga_location+")"
        fig.suptitle(title)
        # Upper raw: low resolution profile
        # Backscatter_plot  Depolarization_plot     Extinction_plot
        legend_plotted=False
        if is_bck_included==1:
            line_styles = cycle(['-', '--', ':', '-.'])
            n_wave, n_time, n_point=self._va_backscatter.shape
            y = self._va_altitude[:] * 0.001
            for t in range(n_time):
                lss=next(line_styles)
                for w in range(n_wave):
                    wave=self._va_wavelength[w]
                    x=self._va_backscatter[w,t,:]*1e6
                    x_err=self._va_error_backscatter[w,t,:]*1e6
                    if n_time == 1:
                        label_txt = str(wave)
                    else:
                        label_txt=str(wave)+ " t=" + str(t)
                    ax[0, 0].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt )
                    #ax[0,0].plot(x, y, color=set_profile_color(wave), ls=lss, label=label_txt)
                    ax[0,0].set_ylabel("Height [km]")
                    ax[0,0].set_xlabel("Backscatter [Mm$^{-1}$sr$^{-1}$]")
                    ax[0,0].legend()
                    ax[0,0].grid(True)
            legend_plotted = True
        else:
            ax[0,0].axis("off")
        if is_dep_included==1:
            line_styles = cycle(['-', '--', ':', '-.'])
            n_wave, n_time, n_point=self._va_volumedepolarization.shape
            y = self._va_altitude[:] * 0.001
            for t in range(n_time):
                lss=next(line_styles)
                for w in range(n_wave):
                    wave=self._va_wavelength[w]
                    #print(wave,set_profile_color(wave))
                    x=self._va_volumedepolarization[w,t,:]
                    x_err=self._va_error_volumedepolarization[w,t,:]
                    if n_time == 1:
                        label_txt = str(wave)
                    else:
                        label_txt=str(wave)+ " t=" + str(t)
                    ax[0, 1].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
                    #ax[0,1].plot(x, y, color=set_profile_color(wave), ls=lss, label=label_txt)
                    ax[0,1].set_xlabel("Depolarization")
                    if not legend_plotted:
                        ax[0,1].set_ylabel("Height [km]")
                        ax[0,1].legend()
                    ax[0,1].grid(True)
            legend_plotted = True
        else:
            ax[0,1].axis("off")
        if is_ext_included==1:
            line_styles = cycle(['-', '--', ':', '-.'])
            n_wave, n_time, n_point=self._va_extinction.shape
            y = self._va_altitude[:] * 0.001
            for t in range(n_time):
                lss=next(line_styles)
                for w in range(n_wave):
                    wave=self._va_wavelength[w]
                    #print(wave,set_profile_color(wave))
                    x=self._va_extinction[w,t,:]*1e6
                    x_err=self._va_error_extinction[w,t,:]*1e6

                    if n_time == 1:
                        label_txt = str(wave)
                    else:
                        label_txt=str(wave)+ " t=" + str(t)
                    ax[0,2].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
                    #ax[0,2].plot(x, y, color=set_profile_color(wave), ls=lss, label=label_txt)
                    ax[0,2].set_xlabel("Extinction [Mm$^{-1}$]")
                    if not legend_plotted:
                        ax[0,2].set_ylabel("Height [km]")
                        ax[0,2].legend()
                    ax[0,2].grid(True)
            #legend_plotted = False
        else:
            ax[0, 2].axis("off")

        fig.text(
            0.5,
            0.02,
            "Filename: "+self.filename,
            ha="center",
            va="bottom",
            fontsize=8
        )

        plt.tight_layout()
        plt.show()