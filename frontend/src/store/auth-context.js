import React, { useCallback, useState } from "react";

const AuthContext = React.createContext({
  token: "",
  isLoggedIn: false,
  login: (token) => {},
  logout: () => {},
  register: (token) => {}
});

const retrieveStoredToken = () => {
  const storedToken = localStorage.getItem("token");
  return storedToken;
};

export const AuthContextProvider = (props) => {
  const [token, setToken] = useState(retrieveStoredToken() || null)

  const userIsLoggedIn = !!token;

  const logoutHandler = useCallback(() => {
    setToken(null);
    localStorage.removeItem("token");
  }, []);

  const loginHandler = (token) => {
    setToken(token);
    localStorage.setItem("token", token);
  };

  const registerHandler = (token) => {
    setToken(token);
    localStorage.setItem("token", token);
  }

  const contextValue = {
      token: token,
      isLoggedIn: userIsLoggedIn,
      login: loginHandler,
      logout: logoutHandler,
      register: registerHandler
  };
  return (
      <AuthContext.Provider value={contextValue}>
          {props.children}
      </AuthContext.Provider>
  );
};

export default AuthContext;
