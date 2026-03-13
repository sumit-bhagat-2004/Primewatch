'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { authStorage } from '@/lib/auth';
import toast from 'react-hot-toast';
import type { User, WatchlistItem, WatchlistItemCreate } from '@/types';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<WatchlistItem | null>(null);

  // Form state
  const [tokenSymbol, setTokenSymbol] = useState('');
  const [targetPrice, setTargetPrice] = useState('');
  const [notes, setNotes] = useState('');

  useEffect(() => {
    if (!authStorage.isAuthenticated()) {
      router.push('/login');
      return;
    }

    loadUserData();
  }, [router]);

  const loadUserData = async () => {
    try {
      // Load user profile first
      const userData = await api.user.getProfile();
      setUser(userData);

      // Then load watchlist based on user role
      const watchlistData = userData.role === 'admin'
        ? await api.admin.getAllWatchlists()
        : await api.watchlist.getAll();
      setWatchlist(watchlistData);
    } catch (error) {
      toast.error('Failed to load data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    authStorage.removeToken();
    toast.success('Logged out successfully');
    router.push('/login');
  };

  const handleAddItem = () => {
    setEditingItem(null);
    setTokenSymbol('');
    setTargetPrice('');
    setNotes('');
    setIsFormOpen(true);
  };

  const handleEditItem = (item: WatchlistItem) => {
    setEditingItem(item);
    setTokenSymbol(item.token_symbol);
    setTargetPrice(item.target_price.toString());
    setNotes(item.notes || '');
    setIsFormOpen(true);
  };

  const handleSubmitForm = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!tokenSymbol || !targetPrice) {
      toast.error('Token symbol and target price are required');
      return;
    }

    try {
      if (editingItem) {
        await api.watchlist.update(editingItem.id, {
          token_symbol: tokenSymbol,
          target_price: parseFloat(targetPrice),
          notes: notes || undefined,
        });
        toast.success('Watchlist item updated!');
      } else {
        await api.watchlist.create({
          token_symbol: tokenSymbol,
          target_price: parseFloat(targetPrice),
          notes: notes || undefined,
        });
        toast.success('Watchlist item added!');
      }
      setIsFormOpen(false);
      loadUserData();
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Operation failed';
      toast.error(message);
    }
  };

  const handleDeleteItem = async (id: string) => {
    if (!confirm('Are you sure you want to delete this item?')) {
      return;
    }

    try {
      await api.watchlist.delete(id);
      toast.success('Watchlist item deleted!');
      loadUserData();
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Delete failed';
      toast.error(message);
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-gray-900">
                PrimeWatch Dashboard
              </h1>
              {user && (
                <p className="mt-1 text-sm text-gray-600">
                  Welcome, {user.email} ({user.role})
                </p>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Add Button */}
        <div className="mb-6">
          <button
            onClick={handleAddItem}
            className="rounded-md bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-500"
          >
            + Add Watchlist Item
          </button>
        </div>

        {/* Form Modal */}
        {isFormOpen && (
          <div className="fixed inset-0 z-10 overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4">
              <div className="fixed inset-0 bg-gray-500 bg-opacity-75" onClick={() => setIsFormOpen(false)}></div>
              <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6">
                <h3 className="text-lg font-semibold mb-4">
                  {editingItem ? 'Edit Watchlist Item' : 'Add Watchlist Item'}
                </h3>
                <form onSubmit={handleSubmitForm} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Token Symbol
                    </label>
                    <input
                      type="text"
                      value={tokenSymbol}
                      onChange={(e) => setTokenSymbol(e.target.value)}
                      className="w-full rounded-md border-gray-300 border px-3 py-2"
                      placeholder="e.g., BTC, ETH"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Target Price
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={targetPrice}
                      onChange={(e) => setTargetPrice(e.target.value)}
                      className="w-full rounded-md border-gray-300 border px-3 py-2"
                      placeholder="e.g., 65000"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Notes (Optional)
                    </label>
                    <textarea
                      value={notes}
                      onChange={(e) => setNotes(e.target.value)}
                      className="w-full rounded-md border-gray-300 border px-3 py-2"
                      rows={3}
                      placeholder="Add your notes here..."
                    />
                  </div>
                  <div className="flex gap-3 justify-end">
                    <button
                      type="button"
                      onClick={() => setIsFormOpen(false)}
                      className="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-300"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="rounded-md bg-primary-600 px-4 py-2 text-sm font-semibold text-white hover:bg-primary-500"
                    >
                      {editingItem ? 'Update' : 'Add'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}

        {/* Watchlist Table */}
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Token
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Target Price
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Notes
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {watchlist.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                    No watchlist items yet. Add your first one!
                  </td>
                </tr>
              ) : (
                watchlist.map((item) => (
                  <tr key={item.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-semibold text-gray-900">{item.token_symbol}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                      ${item.target_price.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 text-gray-700">
                      {item.notes || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(item.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleEditItem(item)}
                        className="text-primary-600 hover:text-primary-900 mr-4"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteItem(item.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
