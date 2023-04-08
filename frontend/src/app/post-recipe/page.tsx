import LargeHeading from '@/components/ui/LargeHeading';
import React from 'react';
import { Metadata } from 'next'
import RecipeForm from '@/components/RecipeForm';

export const metadata: Metadata = {
  title: 'Goodeats | Post recipe',
}

const page: React.FC = () => {
  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <div className='h-full gap-6 flex flex-col justify-start items-center'>

          <LargeHeading size='lg' className='text-black'>
            Post recipe
          </LargeHeading>

          <RecipeForm />

        </div>
      </div>
    </div>
  );
}

export default page
