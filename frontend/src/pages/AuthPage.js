import { useHistory } from "react-router-dom";
import { useEffect } from "react";

import AuthForm from "../components/Auth/AuthForm";
import useHttp from "../hooks/use-http";
import { Login } from "../lib/api";

const AuthPage = () => {
  const { sendRequest, status } = useHttp(Login);
  const history = useHistory();

  useEffect(() => {
    if (status === "completed") {
      history.push("/auth");
    }
  }, [status, history]);

  const loginHandler = (loginData) => {
    sendRequest(loginData);
  };
  return <AuthForm />;
};

export default AuthPage;
