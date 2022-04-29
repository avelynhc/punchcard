import {Switch, Route, Redirect} from 'react-router-dom';
import Layout from "./components/Layout/Layout";
import UserProfile from './components/Profile/UserProfile';
import AuthPage from './pages/AuthPage';
import HomePage from './pages/HomePage';

function App() {
  return (
    <Layout>
      <Switch>
        <Route path='/' exact>
          <HomePage />
        </Route>
        <Route path='/auth' exact>
          <AuthPage />
        </Route>
        <Route path='/profile' exact>
          <UserProfile />
        </Route>
        <Route path='*'>
          <Redirect to='/' />
        </Route>
      </Switch>
    </Layout>
  );
}

export default App;
