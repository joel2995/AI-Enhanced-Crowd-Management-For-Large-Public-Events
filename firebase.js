import {initializeApp} from 'firebase/app';
import {getDatabase, ref, set, push} from 'firebase/database';
import {getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';
import {getStorage} from 'firebase/storage';
import firebase from 'firebase/app';

const firebaseConfig = {
    apiKey: "AIzaSyAZxXa94KAUaj8uI6FqcX2VJknTBq8duyU",
    authDomain: "crowd-ad162.firebaseapp.com",
    databaseURL: "https://crowd-ad162-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "crowd-ad162",
    storageBucket: "crowd-ad162.appspot.com",
    messagingSenderId: "830817651299",
    appId: "1:830817651299:web:935dea65357ddf7532c656",
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const auth = getAuth(app);
export const storage = getStorage(app);
export {database, ref, set, push, auth, createUserWithEmailAndPassword, signInWithEmailAndPassword };