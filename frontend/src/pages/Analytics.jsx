import { useState, useEffect } from 'react';
import { useHabits } from '../contexts/HabitsContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { 
  TrendingUp, 
  Calendar, 
  Target, 
  Flame,
  Award,
  Activity
} from 'lucide-react';

const Analytics = () => {
  const { habits, fetchHabitAnalytics, loading } = useHabits();
  const [analytics, setAnalytics] = useState([]);
  const [selectedPeriod, setSelectedPeriod] = useState('30');
  const [selectedHabit, setSelectedHabit] = useState('all');
  
  useEffect(() => {
    loadAnalytics();
  }, [selectedPeriod]);
  
  const loadAnalytics = async () => {
    const data = await fetchHabitAnalytics(parseInt(selectedPeriod));
    setAnalytics(data);
  };
  
  const getFilteredAnalytics = () => {
    if (selectedHabit === 'all') return analytics;
    return analytics.filter(item => item.habit_id.toString() === selectedHabit);
  };
  
  const getOverallStats = () => {
    const filtered = getFilteredAnalytics();
    if (filtered.length === 0) return null;
    
    const totalDays = parseInt(selectedPeriod);
    const avgCompletionRate = filtered.reduce((sum, item) => sum + item.completion_rate, 0) / filtered.length;
    const totalCompletions = filtered.reduce((sum, item) => sum + item.completed_days, 0);
    const bestStreak = Math.max(...filtered.map(item => item.longest_streak));
    
    return {
      avgCompletionRate: Math.round(avgCompletionRate),
      totalCompletions,
      bestStreak,
      totalDays,
    };
  };
  
  const getChartData = () => {
    const filtered = getFilteredAnalytics();
    return filtered.map(item => ({
      name: item.habit_name,
      completion_rate: Math.round(item.completion_rate),
      completed_days: item.completed_days,
      current_streak: item.current_streak,
      longest_streak: item.longest_streak,
    }));
  };
  
  const stats = getOverallStats();
  const chartData = getChartData();
  
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
          <h1 className="text-3xl font-bold text-foreground">Analytics</h1>
          <p className="text-muted-foreground">
            Analyze your habit patterns and track your progress over time
          </p>
        </div>
        
        <div className="flex space-x-2">
          <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7">Last 7 days</SelectItem>
              <SelectItem value="30">Last 30 days</SelectItem>
              <SelectItem value="90">Last 90 days</SelectItem>
              <SelectItem value="365">Last year</SelectItem>
            </SelectContent>
          </Select>
          
          <Select value={selectedHabit} onValueChange={setSelectedHabit}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All habits</SelectItem>
              {habits.map(habit => (
                <SelectItem key={habit.id} value={habit.id.toString()}>
                  {habit.icon} {habit.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
      
      {/* Overview Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Completion Rate</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.avgCompletionRate}%</div>
              <p className="text-xs text-muted-foreground">
                over {selectedPeriod} days
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Completions</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalCompletions}</div>
              <p className="text-xs text-muted-foreground">
                completed habits
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Best Streak</CardTitle>
              <Flame className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.bestStreak}</div>
              <p className="text-xs text-muted-foreground">
                consecutive days
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Consistency Score</CardTitle>
              <Award className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stats.avgCompletionRate >= 80 ? 'A' : 
                 stats.avgCompletionRate >= 60 ? 'B' : 
                 stats.avgCompletionRate >= 40 ? 'C' : 'D'}
              </div>
              <p className="text-xs text-muted-foreground">
                performance grade
              </p>
            </CardContent>
          </Card>
        </div>
      )}
      
      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Completion Rate Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Completion Rates
            </CardTitle>
            <CardDescription>
              Percentage of days each habit was completed
            </CardDescription>
          </CardHeader>
          <CardContent>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="name" 
                    tick={{ fontSize: 12 }}
                    interval={0}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis />
                  <Tooltip 
                    formatter={(value) => [`${value}%`, 'Completion Rate']}
                  />
                  <Bar dataKey="completion_rate" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-64 text-muted-foreground">
                No data available for the selected period
              </div>
            )}
          </CardContent>
        </Card>
        
        {/* Streak Comparison */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Flame className="h-5 w-5 mr-2" />
              Streak Performance
            </CardTitle>
            <CardDescription>
              Current vs longest streaks for each habit
            </CardDescription>
          </CardHeader>
          <CardContent>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="name" 
                    tick={{ fontSize: 12 }}
                    interval={0}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="current_streak" fill="#10B981" name="Current Streak" />
                  <Bar dataKey="longest_streak" fill="#F59E0B" name="Longest Streak" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-64 text-muted-foreground">
                No data available for the selected period
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      
      {/* Detailed Analytics Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Calendar className="h-5 w-5 mr-2" />
            Detailed Analytics
          </CardTitle>
          <CardDescription>
            Comprehensive breakdown of habit performance
          </CardDescription>
        </CardHeader>
        <CardContent>
          {analytics.length > 0 ? (
            <div className="space-y-4">
              {getFilteredAnalytics().map((item) => (
                <div key={item.habit_id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                      <Target className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                      <h4 className="font-medium">{item.habit_name}</h4>
                      <p className="text-sm text-muted-foreground">
                        {item.completed_days} of {item.total_days} days completed
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="text-center">
                      <div className="text-lg font-bold">{Math.round(item.completion_rate)}%</div>
                      <div className="text-xs text-muted-foreground">Completion</div>
                    </div>
                    
                    <div className="text-center">
                      <div className="text-lg font-bold">{item.current_streak}</div>
                      <div className="text-xs text-muted-foreground">Current Streak</div>
                    </div>
                    
                    <div className="text-center">
                      <div className="text-lg font-bold">{item.longest_streak}</div>
                      <div className="text-xs text-muted-foreground">Best Streak</div>
                    </div>
                    
                    <Badge 
                      variant={item.completion_rate >= 80 ? "default" : 
                               item.completion_rate >= 60 ? "secondary" : "outline"}
                    >
                      {item.completion_rate >= 80 ? 'Excellent' : 
                       item.completion_rate >= 60 ? 'Good' : 
                       item.completion_rate >= 40 ? 'Fair' : 'Needs Work'}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Calendar className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium text-foreground mb-2">No analytics data</h3>
              <p className="text-muted-foreground">
                Start tracking habits to see your analytics here
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Analytics;

