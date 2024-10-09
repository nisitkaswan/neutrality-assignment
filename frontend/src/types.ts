export interface User {
  id: string;
  name: string;
  zipcode: string;
  city: string;
  state: string;
}

export interface Users {
  [id: string]: User;
}