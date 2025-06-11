import { useState, useEffect } from 'react';
import { useHabits } from '../contexts/HabitsContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  Target, 
  TrendingUp, 
  Calendar, 
  CheckCircle2, 
  Plus,
  Flame,
  Trophy,
  Clock
} from 'lucide-react';

const Dashboard = () => {
  const { 
    habits, 
    dashboardStats, 
    entries, 
    fetchEntriesForDate, 
    createEntry, 
    updateEntry,
    loading 
  } = useHabits();
  
  const [todayEntries, setTodayEntries] = useState([]);
  const today = new Date().toISOString().split('T')[0];
  
  useEffect(() => {
    fetchEntriesForDate(today).then(setTodayEntries);
  }, [today]);
  
  const handleToggleHabit = async (habit) => {
    const existingEntry = todayEntries.find(entry => entry.habit_id === habit.id);
    
    if (existingEntry) {
      // Update existing entry
      await updateEntry(existingEntry.id, {
        completed: !existingEntry.completed,
        value: habit.target_value,
      });
    } else {
      // Create new entry
      await createEntry({
        habit_id: habit.id,
        date: today,
        completed: true,
        value: habit.target_value,
      });
    }
    
    // Refresh today's entries
    const updatedEntries = await fetchEntriesForDate(today);
    setTodayEntries(updatedEntries);
  };
  
  const getHabitStatus = (habit) => {
    const entry = todayEntries.find(e => e.habit_id === habit.id);
    return entry?.completed || false;
  };
  
  const todayProgress = dashboardStats ? 
    (dashboardStats.today_total > 0 ? (dashboardStats.today_completed / dashboardStats.today_total) * 100 : 0) : 0;
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground">
            Track your daily habits and see your progress
          </p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Habit
        </Button>
      </div>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Today's Progress</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboardStats?.today_completed || 0}/{dashboardStats?.today_total || 0}
            </div>
            <Progress value={todayProgress} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-2">
              {Math.round(todayProgress)}% completed
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Current Streak</CardTitle>
            <Flame className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats?.current_streak || 0}</div>
            <p className="text-xs text-muted-foreground">
              days in a row
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Habits</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats?.active_habits || 0}</div>
            <p className="text-xs text-muted-foreground">
              out of {dashboardStats?.total_habits || 0} total
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Completions</CardTitle>
            <Trophy className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardStats?.total_completions || 0}</div>
            <p className="text-xs text-muted-foreground">
              all time
            </p>
          </CardContent>
        </Card>
      </div>
      
      {/* Today's Habits */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Calendar className="h-5 w-5 mr-2" />
            Today's Habits
          </CardTitle>
          <CardDescription>
            Complete your daily habits to maintain your streaks
          </CardDescription>
        </CardHeader>
        <CardContent>
          {habits.length === 0 ? (
            <div className="text-center py-8">
              <Target className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium text-foreground mb-2">No habits yet</h3>
              <p className="text-muted-foreground mb-4">
                Create your first habit to start tracking your progress
              </p>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Add Your First Habit
              </Button>
            </div>
          ) : (
            <div className="space-y-3">
              {habits.filter(habit => habit.is_active).map((habit) => {
                const isCompleted = getHabitStatus(habit);
                return (
                  <div
                    key={habit.id}
                    className={`flex items-center justify-between p-4 rounded-lg border transition-colors ${
                      isCompleted 
                        ? 'bg-green-50 border-green-200 dark:bg-green-950 dark:border-green-800' 
                        : 'bg-card border-border hover:bg-accent'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <div 
                        className="w-8 h-8 rounded-lg flex items-center justify-center text-white text-lg"
                        style={{ backgroundColor: habit.color }}
                      >
                        {habit.icon}
                      </div>
                      <div>
                        <h4 className="font-medium text-foreground">{habit.name}</h4>
                        <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                          <span>{habit.habit_type === 'boolean' ? 'Complete' : `${habit.target_value} ${habit.unit || 'times'}`}</span>
                          {habit.current_streak > 0 && (
                            <Badge variant="secondary" className="text-xs">
                              <Flame className="h-3 w-3 mr-1" />
                              {habit.current_streak} day streak
                            </Badge>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    <Button
                      variant={isCompleted ? "default" : "outline"}
                      size="sm"
                      onClick={() => handleToggleHabit(habit)}
                      className={isCompleted ? "bg-green-600 hover:bg-green-700" : ""}
                    >
                      {isCompleted ? (
                        <>
                          <CheckCircle2 className="h-4 w-4 mr-2" />
                          Completed
                        </>
                      ) : (
                        <>
                          <Clock className="h-4 w-4 mr-2" />
                          Mark Done
                        </>
                      )}
                    </Button>
                  </div>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;

