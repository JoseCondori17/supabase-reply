'use client';

interface ViewDataProps {
  data: Record<string, any>[];
}

export function ViewData({ data }: ViewDataProps) {
  if (!data || data.length === 0) {
    return <div className="p-4 text-muted-foreground">No results</div>;
  }

  const headers = Object.keys(data[0]);

  return (
    <div className="overflow-auto h-full w-full p-2">
      <table className="min-w-full border border-gray-300 text-sm">
        <thead className="bg-gray-100">
          <tr>
            {headers.map((header) => (
              <th key={header} className="px-2 py-1 border border-gray-300 text-left">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx} className="hover:bg-gray-50">
              {headers.map((header) => (
                <td key={header} className="px-2 py-1 border border-gray-300">
                  {String(row[header])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}