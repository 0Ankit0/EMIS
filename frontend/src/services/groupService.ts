import { getAuthToken } from '@/lib/auth-utils';

const API_BASE_URL = '/api/admin';

export interface Group {
    id: number;
    name: string;
    user_count?: number;
    permissions?: number[];
    users?: Array<{ id: number; username: string; email: string }>;
}

export interface GroupCreate {
    name: string;
    permissions?: number[];
}

export interface GroupUpdate {
    name?: string;
    permissions?: number[];
}

const getAuthHeaders = () => ({
    'Authorization': `Token ${getAuthToken()}`,
    'Content-Type': 'application/json',
});

export const getGroups = async (search?: string): Promise<Group[]> => {
    const params = search ? `?search=${encodeURIComponent(search)}` : '';
    const response = await fetch(`${API_BASE_URL}/groups/${params}`, {
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch groups');
    }
    
    return response.json();
};

export const getGroup = async (id: number): Promise<Group> => {
    const response = await fetch(`${API_BASE_URL}/groups/${id}/`, {
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch group');
    }
    
    return response.json();
};

export const createGroup = async (data: GroupCreate): Promise<Group> => {
    const response = await fetch(`${API_BASE_URL}/groups/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create group');
    }
    
    return response.json();
};

export const updateGroup = async (id: number, data: GroupUpdate): Promise<Group> => {
    const response = await fetch(`${API_BASE_URL}/groups/${id}/`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(data),
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update group');
    }
    
    return response.json();
};

export const deleteGroup = async (id: number): Promise<void> => {
    const response = await fetch(`${API_BASE_URL}/groups/${id}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
        throw new Error('Failed to delete group');
    }
};

export const addUserToGroup = async (groupId: number, userId: number): Promise<Group> => {
    const response = await fetch(`${API_BASE_URL}/groups/${groupId}/add_user/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ user_id: userId }),
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to add user to group');
    }
    
    return response.json();
};

export const removeUserFromGroup = async (groupId: number, userId: number): Promise<Group> => {
    const response = await fetch(`${API_BASE_URL}/groups/${groupId}/remove_user/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ user_id: userId }),
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to remove user from group');
    }
    
    return response.json();
};
