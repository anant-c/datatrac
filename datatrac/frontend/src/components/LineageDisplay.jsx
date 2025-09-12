import PropTypes from 'prop-types';
import { ArrowUpRight, ArrowDownRight, Loader } from 'lucide-react';

export function LineageDisplay({ lineage, isLoading, onSelectDataset }) {
    if (isLoading) {
        return (
            <div className="flex items-center justify-center p-4 text-gray-500">
                <Loader className="animate-spin mr-2" size={20} /> Loading lineage...
            </div>
        );
    }

    const hasParents = lineage.parents && lineage.parents.length > 0;
    const hasChildren = lineage.children && lineage.children.length > 0;

    if (!hasParents && !hasChildren) {
        return <p className="text-sm text-gray-500 mt-4 p-4 bg-gray-50 rounded-md">No lineage information available.</p>;
    }

    const LineageItem = ({ dataset, type }) => (
        <li className="flex items-center">
            {type === 'parent' ? <ArrowUpRight className="text-gray-400 mr-2" size={18} /> : <ArrowDownRight className="text-gray-400 mr-2" size={18} />}
            <a
                href="#"
                onClick={(e) => {
                    e.preventDefault();
                    onSelectDataset(dataset);
                }}
                className="text-blue-600 hover:underline hover:text-blue-800"
            >
                {dataset.name}
            </a>
        </li>
    );

    return (
        <div className="mt-4 p-4 bg-gray-50 rounded-md border">
            <h4 className="font-bold text-gray-800 mb-2">Dataset Lineage</h4>
            <div className="space-y-3">
                {hasParents && (
                    <div>
                        <h5 className="text-sm font-semibold text-gray-600">Parents (Derived From)</h5>
                        <ul className="mt-1 space-y-1 pl-2">{lineage.parents.map(p => <LineageItem key={p.hash} dataset={p} type="parent" />)}</ul>
                    </div>
                )}
                {hasChildren && (
                    <div>
                        <h5 className="text-sm font-semibold text-gray-600">Children (Derived To)</h5>
                        <ul className="mt-1 space-y-1 pl-2">{lineage.children.map(c => <LineageItem key={c.hash} dataset={c} type="child" />)}</ul>
                    </div>
                )}
            </div>
        </div>
    );
}

LineageDisplay.propTypes = {
    lineage: PropTypes.object.isRequired,
    isLoading: PropTypes.bool.isRequired,
    onSelectDataset: PropTypes.func.isRequired,
};