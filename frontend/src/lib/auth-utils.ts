import Cookies from 'js-cookie';
import CryptoJS from 'crypto-js';

const SECRET_KEY = process.env.NEXT_PUBLIC_AUTH_SECRET || 'default-secret-key-change-me';
const TOKEN_KEY = 'auth_token';

export const encryptToken = (token: string): string => {
    return CryptoJS.AES.encrypt(token, SECRET_KEY).toString();
};

export const decryptToken = (encryptedToken: string): string => {
    try {
        const bytes = CryptoJS.AES.decrypt(encryptedToken, SECRET_KEY);
        return bytes.toString(CryptoJS.enc.Utf8);
    } catch (error) {
        console.error("Failed to decrypt token", error);
        return '';
    }
};

export const setAuthToken = (token: string) => {
    const encrypted = encryptToken(token);
    // Set cookie for 7 days, secure in production
    Cookies.set(TOKEN_KEY, encrypted, {
        expires: 7,
        secure: window.location.protocol === 'https:',
        sameSite: 'Strict'
    });
};

export const getAuthToken = (): string | null => {
    const encrypted = Cookies.get(TOKEN_KEY);
    if (encrypted) {
        const decrypted = decryptToken(encrypted);
        return decrypted || null;
    }
    return null;
};

export const removeAuthToken = () => {
    Cookies.remove(TOKEN_KEY);
};

export const isAuthenticated = (): boolean => {
    return !!Cookies.get(TOKEN_KEY);
};
