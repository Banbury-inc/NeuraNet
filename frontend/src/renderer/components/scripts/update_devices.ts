import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { get_current_date_and_time, get_device_name, get_directory_info } from './receiver';


export async function UpdateDevices(username: any) {
  return new Promise(async (resolve, reject) => {
    const user = username || "user";
    const device_number = 0;
    const device_name = get_device_name();
    const files = get_directory_info();
    const date_added = get_current_date_and_time();

    interface SmallDeviceInfo {
      user: string;
      device_number: number;
      device_name: string;
      files: FileInfo[];
      date_added: string;
    }

    interface FileInfo {
      File_Type: string;
      File_Name: string;
      Kind: string;
      Date_Uploaded: string;
      File_Size: number;
      File_Priority: number;
      File_Path: string;
      Original_Device: string;
    }

    const device_info_json: SmallDeviceInfo = {
      user,
      device_number,
      device_name,
      files,
      date_added,
    };

    console.log(device_info_json);

    try {
      const response = await axios.post(`https://website2-v3xlkt54dq-uc.a.run.app/update_devices/${username}/`, device_info_json);
      if (response.status === 200) {
        if (response.data.response === 'success') {
          console.log("Successfully updated devices");
          const result = "success"
          resolve(result);
        } else {
          console.log("Failed to update devices");
          console.log(response.data);
          const result = "fail"
          resolve(result);
        }
      } else if (response.status === 400) {
        console.log("Bad request");
        const result = "fail"
        resolve(result);
      } else if (response.status === 404) {
        console.log("error");
        const result = "fail"
        resolve(result);
      }
      else {
        console.log("error");
        const result = response.data;
        resolve(result);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      const result = "fail"
      resolve(result);
    }
  });
}
