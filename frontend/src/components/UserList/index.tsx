import React, {useEffect} from 'react';
import {useQuery} from '@tanstack/react-query';
import {fetchRandomUsers} from '../../api/users';
import {User} from '../../types';
import {AppDispatch} from "../../store";
import {useDispatch, useSelector} from "react-redux";
import {userSelector, addUsers, setCurrentUsers} from "../../store/userSlice";

const UserList: React.FC = () => {
    const dispatch = useDispatch<AppDispatch>();
    const {users, currentUsers} = useSelector(userSelector);

    const {isLoading, isError, data, refetch} = useQuery<User[]>({
        queryKey: ['randomUsers'],
        queryFn: fetchRandomUsers,
    });

    useEffect(() => {
        if (data) {
            dispatch(setCurrentUsers(data));
            dispatch(addUsers(data));
        }
    }, [data, dispatch]);

    const handleFetchUsers = async () => {
        const newUsers = await refetch();
        if (newUsers.data) {
            dispatch(addUsers(newUsers.data));
            dispatch(setCurrentUsers(newUsers.data));
        }
    };

    if (isError) {
        return <div className="text-red-500">Error fetching users</div>;
    }

    return (
        <div className="p-4">
            <button
                data-test-id="fetch-users-button"
                onClick={handleFetchUsers}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                disabled={isLoading}
            >
                {isLoading ? 'Loading...' : 'Fetch Random Users'}
            </button>
            <div className={`flex flex-row mt-4`}>
                <div className={`flex flex-col`}>
                    <h2 className="text-xl font-bold ">All Unique Users:</h2>
                    <div className={`h-[74vh] overflow-auto`}>
                        <ul data-test-id="all-users-list" className="list-disc pl-5">
                            {(Object.values(users) as User[]).map((user) => (
                                <li key={user.id} className="mt-2" data-test-id={`all-user-${user.id}`}>
                                    {user.name} - {user.zipcode} ({user.city}, {user.state})
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className={`ml-20`}>
                    <h2 className="text-xl font-bold ">Current Users:</h2>
                    <ul data-test-id="current-users-list" className="list-disc pl-5">
                        {currentUsers.map(userId => {
                            const user = users[userId];
                            return (
                                <li key={user.id} className="mt-2" data-test-id={`current-user-${user.id}`}>
                                    {user.name} - {user.zipcode} ({user.city}, {user.state})
                                </li>
                            );
                        })}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default UserList;