import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from 'firebase/auth';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  sendPasswordResetEmail,
  updateProfile,
} from 'firebase/auth';
import { auth } from '../config/firebase';
import { showToast } from '../components/ui/Toast';  // ✅ CHANGED

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
  lastUpdated: number;

  // Actions
  signup: (email: string, password: string, displayName: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
  updateUserProfile: (displayName?: string, photoURL?: string | null) => Promise<void>;
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      loading: true,
      error: null,
      lastUpdated: Date.now(),

      signup: async (email, password, displayName) => {
        try {
          set({ loading: true, error: null });
          const userCredential = await createUserWithEmailAndPassword(auth, email, password);
          await updateProfile(userCredential.user, { displayName });
          set({ user: userCredential.user, loading: false });
          showToast('success', 'Account created successfully!');  // ✅ CHANGED
        } catch (error: any) {
          set({ error: error.message, loading: false });
          showToast('error', error.message);  // ✅ CHANGED
          throw error;
        }
      },

      login: async (email, password) => {
        try {
          set({ loading: true, error: null });
          const userCredential = await signInWithEmailAndPassword(auth, email, password);
          set({ user: userCredential.user, loading: false });
          showToast('success', 'Welcome back!');  // ✅ CHANGED
        } catch (error: any) {
          set({ error: error.message, loading: false });
          showToast('error', 'Invalid email or password');  // ✅ CHANGED
          throw error;
        }
      },

      logout: async () => {
        try {
          await signOut(auth);
          set({ user: null, loading: false });
          showToast('success', 'Logged out successfully');  // ✅ CHANGED
        } catch (error: any) {
          showToast('error', 'Logout failed');  // ✅ CHANGED
          throw error;
        }
      },

      resetPassword: async (email) => {
        try {
          await sendPasswordResetEmail(auth, email);
          showToast('success', 'Password reset email sent!');  // ✅ CHANGED
        } catch (error: any) {
          showToast('error', 'Failed to send reset email');  // ✅ CHANGED
          throw error;
        }
      },

      updateUserProfile: async (displayName, photoURL) => {
        try {
          if (auth.currentUser) {
            // Explicitly handle removal: '' or null means set to null
            const isRemoving = photoURL === '' || photoURL === null;
            const newPhotoURL = isRemoving ? null : (photoURL || auth.currentUser.photoURL);
            const newDisplayName = displayName !== undefined ? (displayName || auth.currentUser.displayName) : auth.currentUser.displayName;

            await updateProfile(auth.currentUser, {
              displayName: newDisplayName || undefined,
              photoURL: newPhotoURL
            });

            await auth.currentUser.reload();

            // Critical: create a shallow copy and explicitly override photoURL 
            // since it might be a non-enumerable getter in the Firebase User object.
            const updatedUser = {
              ...auth.currentUser,
              photoURL: newPhotoURL,
              displayName: newDisplayName || auth.currentUser.displayName
            };

            set({
              user: updatedUser as User,
              lastUpdated: Date.now(),
              loading: false
            });

            showToast('success', 'Profile updated!');
          }
        } catch (error: any) {
          showToast('error', 'Failed to update profile');  // ✅ CHANGED
          throw error;
        }
      },

      setUser: (user) => set({ user, loading: false }),
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user }),
    }
  )
);

// Initialize auth listener
onAuthStateChanged(auth, (user) => {
  useAuthStore.getState().setUser(user);
});