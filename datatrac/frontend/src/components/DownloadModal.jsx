import PropTypes from 'prop-types';

export function DownloadModal({ dataset, onClose }) {
    // Note: This assumes a fixed remote user and host.
    // In a real app, this might come from a config.
    const downloadCommand = `scp naruto@taklu.chickenkiller.com:${dataset.registry_path} ./${dataset.name}`;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg">
                <h3 className="text-xl font-bold mb-4 text-blue-700">Download Dataset</h3>
                <p className="mb-4 text-gray-700">
                    Stats updated. To download, copy this command into your terminal:
                </p>
                <div className="bg-gray-100 p-3 rounded-md text-sm font-mono text-gray-800 break-all mb-6">
                    <code>{downloadCommand}</code>
                </div>
                <button
                    onClick={onClose}
                    className="w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
                >
                    Close
                </button>
            </div>
        </div>
    );
}

DownloadModal.propTypes = {
    dataset: PropTypes.object.isRequired,
    onClose: PropTypes.func.isRequired,
};