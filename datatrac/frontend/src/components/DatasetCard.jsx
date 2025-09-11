import PropTypes from 'prop-types';
import { HardDrive, Hash, CheckCircle, XCircle } from 'lucide-react';
import { formatSize } from '../lib/utils';

export function DatasetCard({ dataset, onSelect, isSelected }) {
    return (
        <div
            className={`flex justify-between items-center p-4 my-2 rounded-lg shadow-md cursor-pointer transition-all duration-200 ${isSelected ? 'bg-blue-100 border-l-4 border-blue-500 shadow-lg' : 'bg-white hover:bg-gray-50'}`}
            onClick={() => onSelect(dataset)}
        >
            <div className="flex-grow">
                <h3 className="text-lg font-semibold text-blue-700">{dataset.name}</h3>
                <div className="text-sm text-gray-600 flex items-center gap-2 mt-1">
                    <HardDrive size={16} /> {formatSize(dataset.size_bytes)}
                    <Hash size={16} className="ml-4" /> {dataset.hash.substring(0, 8)}...
                </div>
            </div>
            <div className="flex-shrink-0 ml-4">
                {dataset.is_active ? (
                    <span className="inline-flex items-center gap-1 bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                        <CheckCircle size={14} /> Active
                    </span>
                ) : (
                    <span className="inline-flex items-center gap-1 bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                        <XCircle size={14} /> Deregistered
                    </span>
                )}
            </div>
        </div>
    );
}

DatasetCard.propTypes = {
    dataset: PropTypes.object.isRequired,
    onSelect: PropTypes.func.isRequired,
    isSelected: PropTypes.bool.isRequired,
};