import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import UserList from './components/UserList';
import { Provider } from 'react-redux';
import { store } from './store';

const queryClient = new QueryClient();

const App: React.FC = () => {
  return (<Provider store={store}>
    <QueryClientProvider client={queryClient}>
      <div className="App container mx-auto px-4">
        <h1 className="text-3xl font-bold text-center my-8">Random User List</h1>
        <UserList />
      </div>
    </QueryClientProvider>
    </Provider>
  );
};

export default App;