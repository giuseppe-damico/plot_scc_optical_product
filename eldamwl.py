from dataclasses import dataclass, field, fields
import netCDF4 as nc
import numpy as np
from typing import List
import matplotlib.pyplot as plt
from itertools import cycle
import os

# def set_profile_color(wave):
#    wave_int = int(wave)
#    if wave_int == 1064:
#        color = 'red'
#    elif wave_int == 532:
#        color = 'green'
#    else:
#        color = 'blue'
#    return color

def merge_two_string_arrays(str1, str2):
    merged = np.array(
        list(dict.fromkeys(
            x for x in np.concatenate([str1, str2])
            if isinstance(x, str) and x.strip()
        )),
        dtype=object
    )
    return merged

def get_group_data_from_netcdf_dataset(dc, dataset, group_name: str):
    grp = dataset
    for name in group_name.strip("/").split("/"):
        if name not in grp.groups:
            print(f"{name} group does not exist")
            return
        grp = grp.groups[name]

    for f in fields(dc):
        # print("NAME: ", f.name)
        # Getting global attributes
        # Getting all the dataclass members whose name starts with "_ga_"
        if f.name.startswith("_ga_"):
            member_name = f.name
            member_type = f.type
            attribute_name = member_name.replace("_ga_", "")
            #print("GROUP GA:", attribute_name)
            if attribute_name in grp.ncattrs():
                # Read the attribute value
                setattr(dc, member_name, member_type(grp.getncattr(attribute_name)))
            else:
                print(f"Attribute '{attribute_name}' not found in the group {group_name}.")

        # Getting variables
        # Getting all the dataclass members whose name starts with "_va_"
        elif f.name.startswith("_va_"):
            member_name = f.name
            # member_type = f.type
            variable_name = member_name.replace("_va_", "")

            if variable_name not in grp.variables:
                print(f"Variable '{variable_name}' not found in group '{group_name}'")
                continue

            var = grp.variables[variable_name]

            # String values
            if var.dtype is str or (
                    isinstance(var.dtype, np.dtype) and var.dtype.kind in ("O", "S", "U")):
                buffer = np.array(var[:], dtype=object, copy=True)

                if isinstance(var.dtype, np.dtype) and var.dtype.kind in ("S", "U") and buffer.ndim > 1:
                    buffer = np.array(
                        ["".join(row).strip() for row in buffer],
                        dtype=object
                    )
                setattr(dc, member_name, buffer)
                continue

            # Numeric values
            fill_value = getattr(var, "_FillValue", None)
            if np.issubdtype(var.dtype, np.floating):
                target_dtype = var.dtype
            else:
                target_dtype = np.float64

            buffer = np.array(var[:], dtype=target_dtype,order="C",copy=True)

            if fill_value is not None and np.issubdtype(buffer.dtype, np.floating):
                buffer[buffer == fill_value] = np.nan

            setattr(dc, member_name, buffer)


@dataclass
class EldamwlMetaDataBackscatter:
    def from_netcdf_dataset(self, dataset, group_name: str):
        get_group_data_from_netcdf_dataset(self, dataset, group_name)

    name: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_retrieval_method: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_retrieval_method: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_calibration_range_search_algorithm: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_nv: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_calibration_search_range: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_calibration_value: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_evaluation_algorithm: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_time: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_calibration_range: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_level: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_altitude: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_assumed_particle_lidar_ratio: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

@dataclass
class EldamwlMetaDataExtinction:

    name: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_retrieval_method: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_angstroem_exponent: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_evaluation_algorithm: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _ga_overlap_correction_file: str = ""

@dataclass
class EldamwlMetaDataVolumeDepolarization:
    name: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_retrieval_method: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_retrieval_method: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

@dataclass
class EldamwlMetaDataLidarRatio:
    name: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_retrieval_method: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

@dataclass
class EldamwlMetaData:

    def from_netcdf_dataset(self, dataset, group_name: str):
        get_group_data_from_netcdf_dataset(self, dataset, group_name)

    _va_cloud_mask_type: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_scc_product_type: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_molecular_calculation_source: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    _ga_hoi_system_ID: int = 0
    _ga_hoi_configuration_ID: int = 0
    _ga_molecular_calculation_source_file : str= ""

    _md_extinction_meta_data: List[EldamwlMetaDataExtinction] = field(default_factory=list)
    _md_backscatter_meta_data: List[EldamwlMetaDataBackscatter] = field(default_factory=list)
    _md_volumedepolarization_meta_data: List[EldamwlMetaDataVolumeDepolarization] = field(default_factory=list)
    _md_lidarratio_meta_data: List[EldamwlMetaDataLidarRatio] = field(default_factory=list)

@dataclass
class EldamwlData:
    def from_netcdf_dataset(self, dataset, group_name: str):
        get_group_data_from_netcdf_dataset(self, dataset, group_name)

    _va_level: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_altitude: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_time: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_cloud_mask: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_vertical_res: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_wavelength: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_backscatter: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_backscatter: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_backscatter_meta_data: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_extinction: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_extinction: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_extinction_meta_data: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_lidarratio: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_lidarratio: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_lidarratio_meta_data: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_volumedepolarization: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_error_volumedepolarization: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_volumedepolarization_meta_data: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_positive_systematic_error_volumedepolarization: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_negative_systematic_error_volumedepolarization: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

@dataclass
class Eldamwl:
    filename: str = ""
    _ga_measurement_ID: str = ""
    _ga_comment: str = ""
    _ga_title: str = ""
    _ga_source: str = ""
    _ga_references: str =""
    _ga_station_ID: str = ""
    _ga_location: str = ""
    _ga_institution: str = ""
    _ga_PI_name: str = ""
    _ga_PI_affiliation: str = ""
    _ga_PI_affiliation_acronym: str= ""
    _ga_PI_address: str = ""
    _ga_PI_phone: str = ""
    _ga_PI_email: str = ""
    _ga_Data_Originator_name: str = ""
    _ga_Data_Originator_affiliation: str = ""
    _ga_Data_Originator_affiliation_acronym: str = ""
    _ga_Data_Originator_address: str = ""
    _ga_Data_Originator_email: str = ""
    _ga_data_processing_institution: str = ""
    _ga_system: str = ""
    _ga_hoi_system_ID: int = 0
    _ga_hoi_configuration_ID: int = 0
    _ga_processor_name: str = ""

    _va_latitude: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_longitude: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))
    _va_station_altitude: np.ndarray = field(default_factory=lambda: np.zeros((0, 0)))

    _gr_meta_data: EldamwlMetaData = field(default_factory=EldamwlMetaData)

    _gr_lowres_products: EldamwlData = field(default_factory=EldamwlData)
    _gr_highres_products: EldamwlData = field(default_factory=EldamwlData)

    def from_netcdf(self,file_name):
        self.filename = os.path.basename(file_name)
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

                # Getting groups
                # Getting all the dataclass members whose name starts with "_gr_"
                elif f.name.startswith("_gr_"):
                    member_name = f.name
                    #member_type = f.type
                    group_name = member_name.replace("_gr_", "")
                    #print("GROUP=", group_name)
                    value = getattr(self, f.name)
                    value.from_netcdf_dataset(ds, group_name)

            # Getting Metadata
            # Backscatter Metadata
            str1=self._gr_lowres_products._va_backscatter_meta_data.ravel()
            str2=self._gr_highres_products._va_backscatter_meta_data.ravel()
            for md in merge_two_string_arrays(str1, str2):
                dc=EldamwlMetaDataBackscatter()
                dc.name=md
                get_group_data_from_netcdf_dataset(dc, ds, md)
                self._gr_meta_data._md_backscatter_meta_data.append(dc)

            # Extinction Metadata
            str1 = self._gr_lowres_products._va_extinction_meta_data.ravel()
            str2 = self._gr_highres_products._va_extinction_meta_data.ravel()
            for md in merge_two_string_arrays(str1, str2):
                dc = EldamwlMetaDataExtinction()
                dc.name = md
                get_group_data_from_netcdf_dataset(dc, ds, md)
                self._gr_meta_data._md_extinction_meta_data.append(dc)

            # VolumeDepolarization Metadata
            str1 = self._gr_lowres_products._va_volumedepolarization_meta_data.ravel()
            str2 = self._gr_highres_products._va_volumedepolarization_meta_data.ravel()
            for md in merge_two_string_arrays(str1, str2):
                dc = EldamwlMetaDataVolumeDepolarization()
                dc.name = md
                get_group_data_from_netcdf_dataset(dc, ds, md)
                self._gr_meta_data._md_volumedepolarization_meta_data.append(dc)

            # LidarRatio Metadata
            str1 = self._gr_lowres_products._va_lidarratio_meta_data.ravel()
            str2 = self._gr_highres_products._va_lidarratio_meta_data.ravel()
            for md in merge_two_string_arrays(str1, str2):
                dc = EldamwlMetaDataLidarRatio()
                dc.name = md
                get_group_data_from_netcdf_dataset(dc, ds, md)
                self._gr_meta_data._md_lidarratio_meta_data.append(dc)

    def plot(self):
        is_highres_included=0
        is_lowres_included=0
        is_highres_included=0
        is_highres_bck_included = 0
        is_highres_ext_included = 0
        is_highres_dep_included = 0
        is_lowres_bck_included = 0
        is_lowres_ext_included = 0
        is_lowres_dep_included = 0
        alt_lr=[]
        alt_hr = []
        if self._gr_lowres_products._va_altitude.size > 0:
            is_lowres_included=1
            alt_lr=self._gr_lowres_products._va_altitude
        if self._gr_highres_products._va_altitude.size > 0:
            is_highres_included = 1
            alt_hr = self._gr_lowres_products._va_altitude
        if self._gr_lowres_products._va_backscatter.size >0:
            is_lowres_bck_included=1
        if self._gr_highres_products._va_backscatter.size > 0:
            is_highres_bck_included = 1
        if self._gr_lowres_products._va_extinction.size > 0:
            is_lowres_ext_included = 1
        if self._gr_highres_products._va_extinction.size > 0:
            is_highres_ext_included = 1
        if self._gr_lowres_products._va_volumedepolarization.size > 0:
            is_lowres_dep_included = 1
        if self._gr_highres_products._va_volumedepolarization.size > 0:
            is_lowres_dep_included = 1
        n_raw=is_lowres_included+is_highres_included
        n_col=3
        #n_col=is_lowres_bck_included+is_lowres_ext_included+is_lowres_dep_included
        #if is_highres_bck_included+is_highres_ext_included+is_highres_dep_included>n_col:
        #    n_col=is_highres_bck_included+is_highres_ext_included+is_highres_dep_included
        # Creating the needed subplots
        fig, ax = plt.subplots(n_raw, n_col, squeeze=False)
        title="ELDAmwl: "+self._ga_measurement_ID +" ("+self._ga_system +", "+self._ga_location+")"
        fig.suptitle(title)
        # Upper raw: low resolution profile
        # Backscatter_plot  Depolarization_plot     Extinction_plot
        legend_plotted=False
        if is_lowres_bck_included==1:
            line_styles = cycle(['-', '--', ':', '-.'])
            n_wave, n_time, n_point=self._gr_lowres_products._va_backscatter.shape
            for t in range(n_time):
                lss=next(line_styles)
                y = self._gr_lowres_products._va_altitude[t, :]*0.001
                for w in range(n_wave):
                    wave=self._gr_lowres_products._va_wavelength[w]
                    x=self._gr_lowres_products._va_backscatter[w,t,:]*1e6
                    x_err=self._gr_lowres_products._va_error_backscatter[w,t,:]*1e6
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
        if is_lowres_dep_included==1:
            line_styles = cycle(['-', '--', ':', '-.'])
            n_wave, n_time, n_point=self._gr_lowres_products._va_volumedepolarization.shape
            for t in range(n_time):
                lss=next(line_styles)
                y = self._gr_lowres_products._va_altitude[t, :]*0.001
                for w in range(n_wave):
                    wave=self._gr_lowres_products._va_wavelength[w]
                    #print(wave,set_profile_color(wave))
                    x=self._gr_lowres_products._va_volumedepolarization[w,t,:]
                    x_err=self._gr_lowres_products._va_error_volumedepolarization[w,t,:]
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
        if is_lowres_ext_included==1:
            line_styles = cycle(['-', '--', ':', '-.'])
            n_wave, n_time, n_point=self._gr_lowres_products._va_extinction.shape
            for t in range(n_time):
                lss=next(line_styles)
                y = self._gr_lowres_products._va_altitude[t, :]*0.001
                for w in range(n_wave):
                    wave=self._gr_lowres_products._va_wavelength[w]
                    #print(wave,set_profile_color(wave))
                    x=self._gr_lowres_products._va_extinction[w,t,:]*1e6
                    x_err=self._gr_lowres_products._va_error_extinction[w,t,:]*1e6

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
            legend_plotted = False
        else:
            ax[0, 2].axis("off")
        if is_highres_bck_included == 1:
            line_styles = cycle(['-', '--', ':', '-.'])
            n_wave, n_time, n_point = self._gr_highres_products._va_backscatter.shape
            for t in range(n_time):
                lss = next(line_styles)
                y = self._gr_highres_products._va_altitude[t, :] * 0.001
                for w in range(n_wave):
                    wave = self._gr_highres_products._va_wavelength[w]
                    x = self._gr_highres_products._va_backscatter[w, t, :] * 1e6
                    x_err = self._gr_highres_products._va_error_backscatter[w, t, :] * 1e6
                    if n_time == 1:
                        label_txt = str(wave)
                    else:
                        label_txt = str(wave) + " t=" + str(t)
                    ax[1, 0].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
                    # ax[0,0].plot(x, y, color=set_profile_color(wave), ls=lss, label=label_txt)
                    ax[1, 0].set_ylabel("Height [km]")
                    ax[1, 0].set_xlabel("Backscatter [Mm$^{-1}$sr$^{-1}$]")
                    ax[1, 0].legend()
                    ax[1, 0].grid(True)
            legend_plotted = True
        else:
            ax[1, 0].axis("off")
        if is_highres_dep_included == 1:
            line_styles = cycle(['-', '--', ':', '-.'])
            n_wave, n_time, n_point = self._gr_highres_products._va_volumedepolarization.shape
            for t in range(n_time):
                lss = next(line_styles)
                y = self._gr_highres_products._va_altitude[t, :] * 0.001
                for w in range(n_wave):
                    wave = self._gr_highres_products._va_wavelength[w]
                    # print(wave,set_profile_color(wave))
                    x = self._gr_highres_products._va_volumedepolarization[w, t, :]
                    x_err = self._gr_highres_products._va_error_volumedepolarization[w, t, :]
                    if n_time == 1:
                        label_txt = str(wave)
                    else:
                        label_txt = str(wave) + " t=" + str(t)
                    ax[1, 1].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
                    # ax[0,1].plot(x, y, color=set_profile_color(wave), ls=lss, label=label_txt)
                    ax[1, 1].set_xlabel("Depolarization")
                    if not legend_plotted:
                        ax[1, 1].set_ylabel("Height [km]")
                        ax[1, 1].legend()
                    ax[1, 1].grid(True)
            legend_plotted = True
        else:
            ax[1, 1].axis("off")
        if is_highres_ext_included == 1:
            line_styles = cycle(['-', '--', ':', '-.'])
            n_wave, n_time, n_point = self._gr_highres_products._va_extinction.shape
            for t in range(n_time):
                lss = next(line_styles)
                y = self._gr_highres_products._va_altitude[t, :] * 0.001
                for w in range(n_wave):
                    wave = self._gr_highres_products._va_wavelength[w]
                    # print(wave,set_profile_color(wave))
                    x = self._gr_highres_products._va_extinction[w, t, :] * 1e6
                    x_err = self._gr_highres_products._va_error_extinction[w, t, :] * 1e6
                    if n_time == 1:
                        label_txt = str(wave)
                    else:
                        label_txt = str(wave) + " t=" + str(t)
                    ax[1, 2].errorbar(x, y, xerr=x_err, color=set_profile_color(wave), ls=lss, label=label_txt)
                    # ax[0,2].plot(x, y, color=set_profile_color(wave), ls=lss, label=label_txt)
                    ax[1, 2].set_xlabel("Extinction [Mm$^{-1}$]")
                    if not legend_plotted:
                        ax[1, 2].set_ylabel("Height [km]")
                        ax[1, 2].legend()
                    ax[1, 2].grid(True)
            #legend_plotted = True
        else:
            ax[1, 2].axis("off")

        fig.text(
            0.5,
            0.02,
            "Filename: " + self.filename,
            ha="center",
            va="bottom",
            fontsize=8
        )
        plt.tight_layout()
        plt.show()
