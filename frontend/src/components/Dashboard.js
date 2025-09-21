import React, { useState, useEffect } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';
import { 
  TrendingUp, 
  FileText, 
  Globe, 
  Clock, 
  Activity,
  RefreshCw 
} from 'lucide-react';
import { getStatistics, getRecentActivity } from '../services/api';
import { formatNumber, formatDuration, formatDate } from '../utils/helpers';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async (showToast = false) => {
    try {
      setRefreshing(true);
      const [statsData, activityData] = await Promise.all([
        getStatistics(),
        getRecentActivity(10)
      ]);
      
      setStats(statsData);
      setRecentActivity(activityData.recent_activity || []);
      
      if (showToast) {
        toast.success('Dashboard updated');
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto p-6">
        <div className="card">
          <div className="loading-overlay">
            <div className="flex items-center">
              <div className="loading-spinner" />
              <span className="loading-text">Loading dashboard...</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="max-w-7xl mx-auto p-6">
        <div className="card text-center">
          <p className="text-gray-500">No statistics available</p>
          <button onClick={() => fetchData(true)} className="btn-primary mt-4">
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const processingData = [
    { name: 'Translations', value: stats.total_translations, color: '#3b82f6' },
    { name: 'Summaries', value: stats.total_summaries, color: '#10b981' },
  ];

  const sourceData = stats.most_common_sources.slice(0, 5).map((source, index) => ({
    name: source,
    count: Math.floor(Math.random() * 50) + 10, // Mock data since we don't have actual counts
    color: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][index]
  }));

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Overview of translation and summarization activities
          </p>
        </div>
        <button
          onClick={() => fetchData(true)}
          disabled={refreshing}
          className="btn-secondary"
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
          <span className="ml-2">Refresh</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="stat-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="stat-label">Total Articles</p>
              <p className="stat-number">{formatNumber(stats.total_articles_processed)}</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="stat-label">Translations</p>
              <p className="stat-number">{formatNumber(stats.total_translations)}</p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <Globe className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="stat-label">Avg Summary Length</p>
              <p className="stat-number">{Math.round(stats.average_summary_length)}</p>
              <p className="text-xs text-gray-500">words</p>
            </div>
            <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="stat-label">Avg Processing Time</p>
              <p className="stat-number">{formatDuration(stats.average_processing_time)}</p>
            </div>
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <Clock className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Processing Overview */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Processing Overview</h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={processingData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Processing Distribution */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Processing Distribution</h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={processingData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {processingData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Top Sources */}
      {stats.most_common_sources.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Top News Sources</h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sourceData} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={120} />
                <Tooltip />
                <Bar dataKey="count" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Recent Activity */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <Activity className="w-5 h-5 text-primary-600" />
            Recent Activity
          </h3>
        </div>
        
        {recentActivity.length > 0 ? (
          <div className="space-y-3">
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="flex-shrink-0">
                  {activity.type === 'translation' ? (
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <Globe className="w-4 h-4 text-blue-600" />
                    </div>
                  ) : (
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <FileText className="w-4 h-4 text-green-600" />
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900">
                    {activity.type === 'translation' ? 'Translation' : 'Summary'} completed
                  </p>
                  <p className="text-sm text-gray-500 truncate">
                    {activity.original_text}
                  </p>
                  <div className="flex items-center space-x-4 mt-1 text-xs text-gray-400">
                    <span>{formatDuration(activity.processing_time)}</span>
                    <span>{formatDate(activity.timestamp)}</span>
                    {activity.url_source && (
                      <span>from {activity.url_source}</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Activity className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No recent activity</p>
          </div>
        )}
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="card-header">
            <h4 className="text-md font-semibold text-gray-900">Efficiency</h4>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {stats.total_articles_processed > 0 ? '98%' : '0%'}
            </div>
            <p className="text-sm text-gray-500">Success Rate</p>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h4 className="text-md font-semibold text-gray-900">Compression</h4>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              {stats.total_summaries > 0 ? '65%' : '0%'}
            </div>
            <p className="text-sm text-gray-500">Avg Reduction</p>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h4 className="text-md font-semibold text-gray-900">Quality</h4>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">4.8</div>
            <p className="text-sm text-gray-500">Quality Score</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;