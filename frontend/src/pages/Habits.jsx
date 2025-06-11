import { useState } from 'react';
import { useHabits } from '../contexts/HabitsContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  Plus, 
  Edit, 
  Trash2, 
  Target, 
  Flame,
  MoreHorizontal,
  Settings
} from 'lucide-react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';

const Habits = () => {
  const { habits, createHabit, updateHabit, deleteHabit, loading } = useHabits();
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editingHabit, setEditingHabit] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    habit_type: 'boolean',
    target_value: 1,
    unit: '',
    icon: '🎯',
    color: '#3B82F6',
    reminder_enabled: false,
    reminder_time: '',
  });
  
  const habitIcons = ['🎯', '💪', '📚', '🏃', '💧', '🧘', '🎵', '🎨', '💼', '🌱'];
  const habitColors = [
    '#3B82F6', '#EF4444', '#10B981', '#F59E0B', 
    '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'
  ];
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const result = editingHabit 
      ? await updateHabit(editingHabit.id, formData)
      : await createHabit(formData);
    
    if (result.success) {
      setIsCreateDialogOpen(false);
      setIsEditDialogOpen(false);
      setEditingHabit(null);
      resetForm();
    }
  };
  
  const handleEdit = (habit) => {
    setEditingHabit(habit);
    setFormData({
      name: habit.name,
      description: habit.description || '',
      habit_type: habit.habit_type,
      target_value: habit.target_value,
      unit: habit.unit || '',
      icon: habit.icon,
      color: habit.color,
      reminder_enabled: habit.reminder_enabled,
      reminder_time: habit.reminder_time || '',
    });
    setIsEditDialogOpen(true);
  };
  
  const handleDelete = async (habitId) => {
    if (window.confirm('Are you sure you want to delete this habit?')) {
      await deleteHabit(habitId);
    }
  };
  
  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      habit_type: 'boolean',
      target_value: 1,
      unit: '',
      icon: '🎯',
      color: '#3B82F6',
      reminder_enabled: false,
      reminder_time: '',
    });
  };
  
  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };
  
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
          <h1 className="text-3xl font-bold text-foreground">Habits</h1>
          <p className="text-muted-foreground">
            Manage your daily habits and track your progress
          </p>
        </div>
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={resetForm}>
              <Plus className="h-4 w-4 mr-2" />
              Add Habit
            </Button>
          </DialogTrigger>
          <HabitDialog
            formData={formData}
            handleChange={handleChange}
            handleSubmit={handleSubmit}
            habitIcons={habitIcons}
            habitColors={habitColors}
            isEditing={false}
          />
        </Dialog>
      </div>
      
      {/* Habits Grid */}
      {habits.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <Target className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-medium text-foreground mb-2">No habits yet</h3>
            <p className="text-muted-foreground mb-6">
              Create your first habit to start building better daily routines
            </p>
            <Button onClick={() => setIsCreateDialogOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create Your First Habit
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {habits.map((habit) => (
            <Card key={habit.id} className="relative">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div 
                      className="w-10 h-10 rounded-lg flex items-center justify-center text-white text-xl"
                      style={{ backgroundColor: habit.color }}
                    >
                      {habit.icon}
                    </div>
                    <div>
                      <CardTitle className="text-lg">{habit.name}</CardTitle>
                      <div className="flex items-center space-x-2 mt-1">
                        <Badge variant={habit.is_active ? "default" : "secondary"}>
                          {habit.is_active ? "Active" : "Inactive"}
                        </Badge>
                        {habit.current_streak > 0 && (
                          <Badge variant="outline" className="text-orange-600">
                            <Flame className="h-3 w-3 mr-1" />
                            {habit.current_streak}
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="sm">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={() => handleEdit(habit)}>
                        <Edit className="h-4 w-4 mr-2" />
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuItem 
                        onClick={() => handleDelete(habit.id)}
                        className="text-destructive"
                      >
                        <Trash2 className="h-4 w-4 mr-2" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </CardHeader>
              
              <CardContent>
                {habit.description && (
                  <p className="text-sm text-muted-foreground mb-3">
                    {habit.description}
                  </p>
                )}
                
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Type:</span>
                    <span className="capitalize">{habit.habit_type}</span>
                  </div>
                  
                  {habit.habit_type !== 'boolean' && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Target:</span>
                      <span>{habit.target_value} {habit.unit}</span>
                    </div>
                  )}
                  
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Completions:</span>
                    <span>{habit.total_completions}</span>
                  </div>
                  
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Best Streak:</span>
                    <span>{habit.longest_streak} days</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
      
      {/* Edit Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <HabitDialog
          formData={formData}
          handleChange={handleChange}
          handleSubmit={handleSubmit}
          habitIcons={habitIcons}
          habitColors={habitColors}
          isEditing={true}
        />
      </Dialog>
    </div>
  );
};

// Habit Dialog Component
const HabitDialog = ({ formData, handleChange, handleSubmit, habitIcons, habitColors, isEditing }) => {
  return (
    <DialogContent className="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>{isEditing ? 'Edit Habit' : 'Create New Habit'}</DialogTitle>
        <DialogDescription>
          {isEditing ? 'Update your habit details.' : 'Add a new habit to track daily.'}
        </DialogDescription>
      </DialogHeader>
      
      <form onSubmit={handleSubmit}>
        <div className="grid gap-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              placeholder="e.g., Drink 8 glasses of water"
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="description">Description (optional)</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              placeholder="Why is this habit important to you?"
              rows={2}
            />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Icon</Label>
              <div className="grid grid-cols-5 gap-2">
                {habitIcons.map((icon) => (
                  <Button
                    key={icon}
                    type="button"
                    variant={formData.icon === icon ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleChange('icon', icon)}
                    className="h-10 w-10 p-0"
                  >
                    {icon}
                  </Button>
                ))}
              </div>
            </div>
            
            <div className="space-y-2">
              <Label>Color</Label>
              <div className="grid grid-cols-4 gap-2">
                {habitColors.map((color) => (
                  <Button
                    key={color}
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => handleChange('color', color)}
                    className={`h-10 w-10 p-0 border-2 ${
                      formData.color === color ? 'border-foreground' : 'border-border'
                    }`}
                    style={{ backgroundColor: color }}
                  />
                ))}
              </div>
            </div>
          </div>
          
          <div className="space-y-2">
            <Label>Type</Label>
            <Select value={formData.habit_type} onValueChange={(value) => handleChange('habit_type', value)}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="boolean">Yes/No (Complete or not)</SelectItem>
                <SelectItem value="count">Count (Number of times)</SelectItem>
                <SelectItem value="duration">Duration (Time spent)</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          {formData.habit_type !== 'boolean' && (
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="target_value">Target</Label>
                <Input
                  id="target_value"
                  type="number"
                  value={formData.target_value}
                  onChange={(e) => handleChange('target_value', parseFloat(e.target.value))}
                  min="0.1"
                  step="0.1"
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="unit">Unit</Label>
                <Input
                  id="unit"
                  value={formData.unit}
                  onChange={(e) => handleChange('unit', e.target.value)}
                  placeholder={formData.habit_type === 'count' ? 'times, reps, pages' : 'minutes, hours'}
                />
              </div>
            </div>
          )}
        </div>
        
        <DialogFooter>
          <Button type="submit">
            {isEditing ? 'Update Habit' : 'Create Habit'}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  );
};

export default Habits;

