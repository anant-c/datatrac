/**
 * Base URL for the DataTrac API.
 * Ensure your FastAPI backend is running at this address.
 */
export const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Formats a file size in bytes into a human-readable string (KB, MB, GB).
 * @param {number | null} sizeBytes - The size of the file in bytes.
 * @returns {string} The formatted size string.
 */
export const formatSize = (sizeBytes) => {
    if (sizeBytes === null || sizeBytes === undefined) return "N/A";
    if (sizeBytes < 1024) return `${sizeBytes} Bytes`;
    if (sizeBytes < 1024 ** 2) return `${(sizeBytes / 1024).toFixed(2)} KB`;
    if (sizeBytes < 1024 ** 3) return `${(sizeBytes / 1024 ** 2).toFixed(2)} MB`;
    return `${(sizeBytes / 1024 ** 3).toFixed(2)} GB`;
};

/**
 * Formats an ISO date string into a localized, readable format.
 * @param {string | null} isoString - The ISO 8601 date string.
 * @returns {string} The formatted date-time string.
 */
export const formatDateTime = (isoString) => {
    if (!isoString) return "N/A";
    return new Date(isoString).toLocaleString();
};