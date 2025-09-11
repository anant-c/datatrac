import { useState, useEffect, useCallback } from 'react';
import { Header } from './components/Header';
import { DatasetCard } from './components/DatasetCard';
import { TopDatasets } from './components/TopDatasets';
import { DatasetDetail } from './components/DatasetDetail';
import { UploadModal } from './components/UploadModal';
import { API_BASE_URL } from './lib/utils';
import { XCircle } from 'lucide-react';

function App() {
    const [datasets, setDatasets] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedDataset, setSelectedDataset] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);

    // --- FIX FOR THE LOOP ---
    // fetchDatasets ONLY fetches data. It does not depend on selectedDataset.
    const fetchDatasets = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/datasets/`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            setDatasets(data);
        } catch (e) {
            setError("Failed to fetch datasets. Is the backend running?");
        } finally {
            setLoading(false);
        }
    }, []); // Empty dependency array is key!

    // This effect runs the fetch ONCE on mount.
    useEffect(() => {
        fetchDatasets();
    }, [fetchDatasets]);

    // This effect ONLY syncs the selected item if the main list changes.
    useEffect(() => {
        if (selectedDataset) {
            const updatedSelected = datasets.find(ds => ds.hash === selectedDataset.hash);
            setSelectedDataset(updatedSelected || null);
        }
    }, [datasets]);
    // --- END OF FIX ---

    const filteredDatasets = datasets.filter(dataset =>
        dataset.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleDatasetUpdate = (updatedDataset) => {
        setDatasets(prev => prev.map(ds => ds.hash === updatedDataset.hash ? updatedDataset : ds));
    };

    const handleDatasetDeleted = () => {
        setSelectedDataset(null);
        fetchDatasets();
    };

    return (
        <div className="flex flex-col min-h-screen">
            <Header
                onRefresh={fetchDatasets}
                searchTerm={searchTerm}
                onSearchChange={setSearchTerm}
                onUploadClick={() => setIsUploadModalOpen(true)}
            />
            <main className="container mx-auto p-6 flex-grow flex flex-col md:flex-row gap-6">
                {loading && <div className="absolute inset-0 flex items-center justify-center bg-gray-100 bg-opacity-75 z-20"><div className="text-blue-600 text-xl font-semibold">Loading datasets...</div></div>}
                {error && <div className="absolute inset-0 flex items-center justify-center bg-red-100 bg-opacity-90 z-20 text-red-800 text-lg p-4 rounded-lg shadow-lg"><XCircle size={24} className="mr-2" />{error}</div>}
                <section className="flex-grow md:w-2/3 flex flex-col">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">All Datasets</h2>
                    <div className="flex-grow overflow-y-auto pr-2" style={{ maxHeight: 'calc(100vh - 200px)' }}>
                        {filteredDatasets.length > 0 ? (
                            filteredDatasets.map(dataset => (
                                <DatasetCard
                                    key={dataset.hash}
                                    dataset={dataset}
                                    onSelect={setSelectedDataset}
                                    isSelected={selectedDataset?.hash === dataset.hash}
                                />
                            ))
                        ) : !loading && <p className="text-gray-500 text-center py-8">No datasets found.</p>}
                    </div>
                </section>
                <aside className="md:w-1/3 flex-shrink-0 flex flex-col gap-6">
                    <TopDatasets datasets={datasets} onSelect={setSelectedDataset} />
                    <DatasetDetail
                        dataset={selectedDataset}
                        onDatasetUpdate={handleDatasetUpdate}
                        onDatasetDeleted={handleDatasetDeleted}
                    />
                </aside>
            </main>
            {isUploadModalOpen && <UploadModal onClose={() => setIsUploadModalOpen(false)} onUploadSuccess={() => { setIsUploadModalOpen(false); fetchDatasets(); }} />}
        </div>
    );
}

export default App;