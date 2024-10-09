import axios from 'axios';
import { User } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const fetchRandomUsers = async (): Promise<User[]> => {
  const response = await axios.get<User[]>(`${API_URL}/users/`);
  return response.data;
};
