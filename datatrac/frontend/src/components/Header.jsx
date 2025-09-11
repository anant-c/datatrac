import PropTypes from 'prop-types';
import { Search, RefreshCw, File, Upload } from 'lucide-react';

export function Header({ onRefresh, searchTerm, onSearchChange, onUploadClick }) {
    return (
        <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 shadow-lg sticky top-0 z-10">
            <div className="container mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
                <h1 className="text-3xl font-extrabold flex items-center gap-2">
                    <File size={32} /> DataTrac Hub
                </h1>
                <div className="flex items-center gap-4 w-full sm:w-auto">
                    <div className="relative w-full sm:w-72">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                        <input
                            type="text"
                            placeholder="Search datasets..."
                            value={searchTerm}
                            onChange={(e) => onSearchChange(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 rounded-lg bg-blue-700 placeholder-blue-300 text-white focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all"
                        />
                        
                    </div>
                    <button
                        onClick={onRefresh}
                        className="p-2 bg-blue-700 hover:bg-blue-600 rounded-lg transition-colors"
                        title="Refresh Datasets"
                    >
                        <RefreshCw size={20} />
                    </button>
                    <button
                        onClick={onUploadClick}
                        className="py-2 px-4 bg-white text-blue-700 font-semibold rounded-lg hover:bg-gray-200 transition-colors flex items-center gap-2"
                        title="Upload a new dataset"
                    >
                        <Upload size={20} />
                        Upload
                    </button>
                </div>
            </div>
        </header>
    );
}

Header.propTypes = {
    onRefresh: PropTypes.func.isRequired,
    searchTerm: PropTypes.string.isRequired,
    onSearchChange: PropTypes.func.isRequired,
    onUploadClick: PropTypes.func.isRequired, 
};