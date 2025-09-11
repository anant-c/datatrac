import PropTypes from 'prop-types';
import { Download } from 'lucide-react';

export function TopDatasets({ datasets, onSelect }) {
    const topFive = [...datasets]
        .sort((a, b) => b.download_count - a.download_count)
        .slice(0, 5);

    return (
        <div className="p-4 bg-white rounded-lg shadow-md">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Top Downloaded</h2>
            {topFive.length === 0 ? (
                <p className="text-gray-500">No download data yet.</p>
            ) : (
                <ul className="space-y-3">
                    {topFive.map((ds, index) => (
                        <li key={ds.hash}
                            className="flex items-center justify-between p-3 bg-gray-50 rounded-md cursor-pointer hover:bg-blue-50 transition-colors"
                            onClick={() => onSelect(ds)}
                        >
                            <span className="font-medium text-blue-700">{index + 1}. {ds.name}</span>
                            <span className="text-sm text-gray-600 flex items-center gap-1">
                                <Download size={16} /> {ds.download_count}
                            </span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

TopDatasets.propTypes = {
    datasets: PropTypes.array.isRequired,
    onSelect: PropTypes.func.isRequired,
};