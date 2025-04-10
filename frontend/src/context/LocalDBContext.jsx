import { useState, createContext } from "react";
// import { createContext } from "react-router";

const LocalDBContent = createContext({
  counsellors: {},
  setCounsellors: () => {},
});

const LocalDBContextProvider = ({ children }) => {
  const [counsellors, setCounsellors] = useState({});

  return (
    <LocalDBContent.Provider value={{ counsellors, setCounsellors }}>
      {children}
    </LocalDBContent.Provider>
  );
}

export {
  LocalDBContent,
  LocalDBContextProvider
}
