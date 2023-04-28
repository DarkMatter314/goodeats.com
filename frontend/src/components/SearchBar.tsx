'use client'

import { useState } from 'react';
import Icons from '@/components/Icons';
import { useRouter } from 'next/navigation';
import { Button } from '@/ui/Button';

export default function SearchBar() {
  const router = useRouter();
  const [value, setValue] = useState('');

  const handleSearch = () => {
    var query = encodeURIComponent(value);
    router.push(`/recipes?search=${query}`);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSearch();
    }
  };

  return (
    <div className='flex flex-row gap-3 w-full items-center justify-center px-8'>
      <div className='relative w-full'>
        <input
          type='text'
          className='block h-[40px] w-full pl-10 pr-3 py-2 border rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:border-orange-300 focus:ring focus:ring-orange-200 focus:ring-opacity-50 sm:text-sm'
          placeholder='Search recipes'
          value={value}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
        />
        <div className='absolute inset-y-0 left-0 flex items-center pl-3'>
          <Icons.Search className='h-5 w-5 text-gray-400' aria-hidden='true' />
        </div>
      </div>
      <Button variant='default' onClick={() => handleSearch()} className='bg-orange-300 hover:bg-orange-400 text-black'>
        Search
      </Button>
    </div>
  );
}
