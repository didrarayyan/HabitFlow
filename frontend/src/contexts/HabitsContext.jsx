import { createContext, useContext, useReducer, useEffect } from 'react';
import { useAuth } from './AuthContext';

// Habits context
const HabitsContext = createContext();

// Habits reducer
const habitsReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_HABITS':
      return { ...state, habits: action.payload, loading: false };
    case 'ADD_HABIT':
      return { ...state, habits: [...state.habits, action.payload] };
    case 'UPDATE_HABIT':
      return {
        ...state,
        habits: state.habits.map(habit =>
          habit.id === action.payload.id ? action.payload : habit
        ),
      };
    case 'DELETE_HABIT':
      return {
        ...state,
        habits: state.habits.filter(habit => habit.id !== action.payload),
      };
    case 'SET_ENTRIES':
      return { ...state, entries: action.payload };
    case 'ADD_ENTRY':
      return { ...state, entries: [...state.entries, action.payload] };
    case 'UPDATE_ENTRY':
      return {
        ...state,
        entries: state.entries.map(entry =>
          entry.id === action.payload.id ? action.payload : entry
        ),
      };
    case 'SET_DASHBOARD_STATS':
      return { ...state, dashboardStats: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
};

// Initial state
const initialState = {
  habits: [],
  entries: [],
  dashboardStats: null,
  loading: false,
  error: null,
};

// Habits provider component
export const HabitsProvider = ({ children }) => {
  const [state, dispatch] = useReducer(habitsReducer, initialState);
  const { apiCall, isAuthenticated } = useAuth();

  // Load habits when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchHabits();
      fetchDashboardStats();
    }
  }, [isAuthenticated]);

  // Habit operations
  const fetchHabits = async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const habits = await apiCall('/habits/');
      dispatch({ type: 'SET_HABITS', payload: habits });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    }
  };

  const createHabit = async (habitData) => {
    try {
      const habit = await apiCall('/habits/', {
        method: 'POST',
        body: JSON.stringify(habitData),
      });
      dispatch({ type: 'ADD_HABIT', payload: habit });
      return { success: true, habit };
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return { success: false, error: error.message };
    }
  };

  const updateHabit = async (habitId, habitData) => {
    try {
      const habit = await apiCall(`/habits/${habitId}`, {
        method: 'PUT',
        body: JSON.stringify(habitData),
      });
      dispatch({ type: 'UPDATE_HABIT', payload: habit });
      return { success: true, habit };
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return { success: false, error: error.message };
    }
  };

  const deleteHabit = async (habitId) => {
    try {
      await apiCall(`/habits/${habitId}`, { method: 'DELETE' });
      dispatch({ type: 'DELETE_HABIT', payload: habitId });
      return { success: true };
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return { success: false, error: error.message };
    }
  };

  // Entry operations
  const fetchEntriesForDate = async (date) => {
    try {
      const entries = await apiCall(`/habits/entries/date/${date}`);
      dispatch({ type: 'SET_ENTRIES', payload: entries });
      return entries;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return [];
    }
  };

  const createEntry = async (entryData) => {
    try {
      const entry = await apiCall('/habits/entries', {
        method: 'POST',
        body: JSON.stringify(entryData),
      });
      dispatch({ type: 'ADD_ENTRY', payload: entry });
      
      // Refresh dashboard stats
      fetchDashboardStats();
      
      return { success: true, entry };
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return { success: false, error: error.message };
    }
  };

  const updateEntry = async (entryId, entryData) => {
    try {
      const entry = await apiCall(`/habits/entries/${entryId}`, {
        method: 'PUT',
        body: JSON.stringify(entryData),
      });
      dispatch({ type: 'UPDATE_ENTRY', payload: entry });
      
      // Refresh dashboard stats
      fetchDashboardStats();
      
      return { success: true, entry };
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return { success: false, error: error.message };
    }
  };

  // Analytics
  const fetchDashboardStats = async () => {
    try {
      const stats = await apiCall('/analytics/dashboard');
      dispatch({ type: 'SET_DASHBOARD_STATS', payload: stats });
      return stats;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return null;
    }
  };

  const fetchHabitAnalytics = async (days = 30) => {
    try {
      const analytics = await apiCall(`/analytics/habits?days=${days}`);
      return analytics;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      return [];
    }
  };

  const value = {
    ...state,
    fetchHabits,
    createHabit,
    updateHabit,
    deleteHabit,
    fetchEntriesForDate,
    createEntry,
    updateEntry,
    fetchDashboardStats,
    fetchHabitAnalytics,
  };

  return <HabitsContext.Provider value={value}>{children}</HabitsContext.Provider>;
};

// Custom hook to use habits context
export const useHabits = () => {
  const context = useContext(HabitsContext);
  if (!context) {
    throw new Error('useHabits must be used within a HabitsProvider');
  }
  return context;
};

