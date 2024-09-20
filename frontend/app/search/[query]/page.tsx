// app/search/results/[query]/page.js
import { Hub } from '@/components/Hub/Hub';
import { useRouter } from 'next/navigation';

export default function ResultsPage({ params }) {
  const { query } = params; // Get the dynamic query parameter

  // Fetch or filter your data based on the query
  const results = fetchResults(query); // Implement this function to fetch data

  return (
    <Hub param={params} />
    // <div>
    //     <h1>Results for "{query}"</h1>
    //     <ul>
    //         {results.map((result) => (
    //             <li key={result.id}>{result.name}</li> // Display your results here
    //         ))}
    //     </ul>
    // </div>
  );
}

// Example function to simulate fetching results
function fetchResults(query) {
  // Replace this with actual fetching logic
  return [
    { id: 1, name: `Result for ${query} 1` },
    { id: 2, name: `Result for ${query} 2` },
    // Add more mock data as needed
  ];
}
