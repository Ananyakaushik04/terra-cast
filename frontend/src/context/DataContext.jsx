```jsx
import React, { createContext, useState, useEffect, useRef } from 'react';
import axios from 'axios';

export const DataContext = createContext();

export function DataProvider({ children }) {
  const [params, setParams] = useState({
    PM2_5_lag1: 156.0,
    PM10_lag1: 180.0,
    SO2_lag1: 10.0,
    NO2_lag1: 45.0,
    CO_lag1: 1.0,
    O3_lag1: 40.0,
    TEMP: 32.0,
    PRES: 1010.0,
    DEWP: 15.0,
    RAIN: 0.0,
    WSPM: 12.0,
    month: 5,
    hour: 10,
    year: 2015,
    day: 15,
    station: "Dongsi"
  });

  const [stationName, setStationName] = useState("Loading...");
  const [dataTimestamp, setDataTimestamp] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const API_URL = import.meta.env.VITE_API_URL;

  const loadRealData = async (stationFilter = null) => {
    try {
      setIsLoading(true);

      if (!API_URL) {
        throw new Error("VITE_API_URL environment variable is missing.");
      }

      if (typeof stationFilter === 'string') {
        setStationName(`Loading ${stationFilter}...`);
      } else {
        setStationName("Loading random station...");
      }

      // Backend API URL
      const url = `${API_URL.replace(/\/+$/, '')}/dataset/sample`;

      // Add station filter only when selected
      const response = await axios.get(url, {
        params: stationFilter && typeof stationFilter === 'string'
          ? { station: stationFilter }
          : {}
      });

      const data = response.data;

      // Update application data
      setParams(data);

      setStationName(data.station || "Unknown Station");

      // Format timestamp
      if (data.year && data.month && data.day !== undefined && data.hour !== undefined) {
        const timestamp = `${data.year}-${String(data.month).padStart(2, '0')}-${String(data.day).padStart(2, '0')} ${String(data.hour).padStart(2, '0')}:00`;

        setDataTimestamp(timestamp);
      } else {
        setDataTimestamp("");
      }

    } catch (error) {
      console.error("Failed to load real data:", error);

      setStationName("Unable to load station");

    } finally {
      setIsLoading(false);
    }
  };

  const isMounted = useRef(false);

  useEffect(() => {
    if (!isMounted.current) {
      isMounted.current = true;
      loadRealData();
    }

    // Listen for station selection events from Header
    const handleLoadStation = (event) => {
      loadRealData(event.detail);
    };

    window.addEventListener(
      'terracast:load_station',
      handleLoadStation
    );

    return () => {
      window.removeEventListener(
        'terracast:load_station',
        handleLoadStation
      );
    };

  }, []);

  return (
    <DataContext.Provider
      value={{
        params,
        setParams,
        stationName,
        dataTimestamp,
        isLoading,
        loadRealData
      }}
    >
      {children}
    </DataContext.Provider>
  );
}
```
