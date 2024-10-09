import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {User, Users} from '../types';
import {RootState} from "./index.tsx";


interface UserState {
  users: Users;
  currentUsers: string[];
}

const initialState: UserState = {
  users: {},
  currentUsers: [],
};

const userSlice = createSlice({
  name: 'users',
  initialState,
  reducers: {
    setCurrentUsers: (state, action: PayloadAction<User[]>) => {
      state.currentUsers = action.payload.map(user => user.id);
      action.payload.forEach(user => {
        state.users[user.id] = user;
      });
    },
    addUsers: (state, action: PayloadAction<User[]>) => {
      action.payload.forEach(user => {
        if (!state.users[user.id]) {
          state.users[user.id] = user;
        }
      });
    },
  },
});

export const { setCurrentUsers, addUsers } = userSlice.actions;
export const userSelector = (state: RootState) => state.users;
export default userSlice.reducer;