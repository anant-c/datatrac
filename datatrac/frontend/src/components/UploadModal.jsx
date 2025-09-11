import { useState } from 'react';
import PropTypes from 'prop-types';
import { X, UploadCloud, Loader } from 'lucide-react';
import { API_BASE_URL } from '../lib/utils';

export function UploadModal({ onClose, onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [source, setSource] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError("Please select a file to upload.");
            return;
        }
        setIsLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);
        if (source) {
            formData.append('source', source);
        }

        try {
            const response = await fetch(`${API_BASE_URL}/datasets/upload`, {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Upload failed");
            }
            onUploadSuccess();
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg relative">
                <button onClick={onClose} className="absolute top-4 right-4 text-gray-500 hover:text-gray-800">
                    <X size={24} />
                </button>
                <h3 className="text-xl font-bold mb-4 text-blue-700">Upload New Dataset</h3>
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-2">Dataset File*</label>
                        <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                            <div className="space-y-1 text-center">
                                <UploadCloud className="mx-auto h-12 w-12 text-gray-400" />
                                <div className="flex text-sm text-gray-600">
                                    <label htmlFor="file-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none">
                                        <span>Select a file</span>
                                        <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleFileChange} />
                                    </label>
                                </div>
                                {file ? <p className="text-xs text-gray-500">{file.name}</p> : <p className="text-xs text-gray-500">Any file type</p>}
                            </div>
                        </div>
                    </div>
                    <div className="mb-6">
                        <label htmlFor="source" className="block text-sm font-medium text-gray-700">Source URL (Optional)</label>
                        <input
                            type="text"
                            name="source"
                            id="source"
                            value={source}
                            onChange={(e) => setSource(e.target.value)}
                            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                            placeholder="https://example.com/data_source"
                        />
                    </div>
                    {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
                    <div className="flex justify-end gap-4">
                        <button type="button" onClick={onClose} className="py-2 px-4 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300">
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="py-2 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-blue-300 flex items-center"
                        >
                            {isLoading && <Loader className="animate-spin mr-2" size={20} />}
                            {isLoading ? 'Uploading...' : 'Upload'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

UploadModal.propTypes = {
    onClose: PropTypes.func.isRequired,
    onUploadSuccess: PropTypes.func.isRequired,
};