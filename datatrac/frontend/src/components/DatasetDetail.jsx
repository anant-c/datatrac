import { useState } from 'react';
import PropTypes from 'prop-types';
import { Hash, Server, Upload, Calendar, Download, HardDrive, Info, Trash2 } from 'lucide-react';
import { formatSize, formatDateTime, API_BASE_URL } from '../lib/utils';
import { DownloadModal } from './DownloadModal';

// --- CORRECTED PART 1 ---
// Added `onDatasetDeleted` to the list of props being received.
export function DatasetDetail({ dataset, onDatasetUpdate, onDatasetDeleted }) {
    const [showModal, setShowModal] = useState(false);

    const handleDownloadClick = async () => {
        if (!dataset) return;
        try {
            const response = await fetch(`${API_BASE_URL}/datasets/${dataset.hash}/download`, {
                method: 'POST',
            });
            if (!response.ok) throw new Error("Failed to update stats");
            const updatedDataset = await response.json();
            onDatasetUpdate(updatedDataset);
            setShowModal(true);
        } catch (error) {
            console.error("Error triggering download:", error);
            alert("Failed to update download stats.");
        }
    };

    const handleRemoteDelete = async () => {
        if (!dataset) return;
        
        const isConfirmed = window.confirm(
            "Are you sure you want to permanently deregister this dataset? This action cannot be undone."
        );
        if (!isConfirmed) return;

        const adminPassword = window.prompt("Please enter the admin password to proceed:");
        if (!adminPassword) return;

        try {
            const response = await fetch(`${API_BASE_URL}/datasets/${dataset.hash}`, {
                method: 'DELETE',
                headers: { 'X-Admin-Password': adminPassword },
            });
            
            if (response.status === 403) {
                alert("Error: Invalid admin password.");
                return;
            }
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to delete dataset.");
            }
            
            alert("Dataset successfully deregistered.");
            // This now works because the prop is correctly received.
            onDatasetDeleted();

        } catch (error) {
            console.error("Error deleting dataset:", error);
            alert(`Error: ${error.message}`);
        }
    };

    if (!dataset) {
        return (
            <div className="p-6 bg-white rounded-lg shadow-md">
                <div className="flex items-center justify-center h-48 text-gray-500 text-lg">
                    <Info size={24} className="mr-2" /> Select a dataset to view details.
                </div>
            </div>
        );
    }

    return (
        <div className="p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-blue-700 mb-4 break-words">{dataset.name}</h2>
            {/* ... JSX for details remains the same ... */}
            <div className="space-y-3 text-gray-700">
                <p className="flex items-center gap-2"><Hash size={18} /> <span className="font-semibold">Hash:</span> <span className="font-mono text-sm break-all">{dataset.hash}</span></p>
                <p className="flex items-center gap-2"><HardDrive size={18} /> <span className="font-semibold">Size:</span> {formatSize(dataset.size_bytes)}</p>
                <p className="flex items-center gap-2"><Upload size={18} /> <span className="font-semibold">Source:</span> {dataset.source || 'N/A'}</p>
                <p className="flex items-center gap-2"><Calendar size={18} /> <span className="font-semibold">Created:</span> {formatDateTime(dataset.created_at)}</p>
                <p className="flex items-center gap-2"><Download size={18} /> <span className="font-semibold">Downloads:</span> {dataset.download_count}</p>
                <p className="flex items-center gap-2"><Calendar size={18} /> <span className="font-semibold">Last DL:</span> {formatDateTime(dataset.last_downloaded_at)}</p>
            </div>
            {/* The buttons were slightly misaligned, I've fixed the container */}
            <div className="mt-6 flex flex-col sm:flex-row gap-2">
                <button
                    onClick={handleDownloadClick}
                    className="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 disabled:bg-gray-400 transition-colors flex items-center justify-center gap-2"
                    disabled={!dataset.is_active}
                >
                    <Download size={20} /> Request Download
                </button>
                <button
                    onClick={handleRemoteDelete}
                    className="w-full sm:w-auto px-4 py-3 bg-red-600 text-white font-semibold rounded-lg shadow-md hover:bg-red-700 transition-colors flex items-center justify-center gap-2"
                    title="Deregister dataset from the central registry (Admin)"
                >
                    <Trash2 size={20} />
                </button>
            </div>
            {showModal && <DownloadModal dataset={dataset} onClose={() => setShowModal(false)} />}
        </div>
    );
}

DatasetDetail.propTypes = {
    dataset: PropTypes.object,
    onDatasetUpdate: PropTypes.func.isRequired,
    onDatasetDeleted: PropTypes.func.isRequired, // Ensure prop type is defined
};