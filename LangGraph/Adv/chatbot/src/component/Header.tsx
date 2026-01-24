import React from 'react';

const Header: React.FC = () => {
  return (
    <div className="h-14 border-b border-gray-800 flex items-center justify-between px-6">
      <div className="flex items-center space-x-2">
        <select className="bg-[#2a2a2a] text-gray-300 text-sm rounded px-3 py-1 border border-gray-700">
          <option>Greeting</option>
        </select>
      </div>
      <button className="bg-[#2a2a2a] hover:bg-[#3a3a3a] text-gray-300 text-sm px-4 py-1.5 rounded border border-gray-700">
        Share
      </button>
    </div>
  );
};

export default Header;