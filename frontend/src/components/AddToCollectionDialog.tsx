'use client'

import * as Dialog from '@radix-ui/react-dialog';
import Paragraph from '@/ui/Paragraph';
import Icons from '@/components/Icons';
import { IconButton } from '@/ui/Button';
import useSWR from 'swr';
import { useState, useEffect } from 'react';
import Image from 'next/image';
import { toast } from './myUI/toast';

// import { useRouter } from 'next/navigation';

const AddToCollectionDialog = ({username,user_id,recipe_id}:{username:string, user_id:number, recipe_id:number}) => {
  const [feedCollections, setFeedCollections] = useState<any[]>([]);
  // const router = useRouter();
  async function addToMyCollection(collection_id) {

    const data = {user_id, recipe_id, collection_id};
    const response = await fetch(`/api/recipe/collection/${recipe_id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const json = await response.json();
    if (!json.error) {
      toast({
        title: 'Success',
        message: 'Added to collection',
        type: 'success',
        duration: 2000,
      });
    }

  }

useEffect(() => {
    async function fetchCollections() {
      const response = await fetch(`/api/${username}/collections/`);
      const json = await response.json();
      setFeedCollections(json);
    }
    fetchCollections();

},[])


  return (
  <Dialog.Root>
    <Dialog.Trigger asChild>
      <IconButton icon={Icons.Plus} variant='ghost' className='hover:bg-violet-600' />
    </Dialog.Trigger>
    <Dialog.Portal>
      <Dialog.Overlay className='bg-blackA9 data-[state=open]:animate-overlayShow fixed inset-0' />
      <Dialog.Content className="data-[state=open]:animate-contentShow fixed top-[50%] left-[50%] max-h-[85vh] w-[90vw] max-w-[450px] translate-x-[-50%] translate-y-[-50%] rounded-[6px] bg-white p-[25px] shadow-[hsl(206_22%_7%_/_35%)_0px_10px_38px_-10px,_hsl(206_22%_7%_/_20%)_0px_10px_20px_-15px] focus:outline-none">
        <div className='flex flex-row justify-between'>
          <Dialog.Title className='text-[20px] font-bold text-black mb-[15px]'>
            Add to collection
          </Dialog.Title>
          <Dialog.Close asChild>
            <IconButton icon={Icons.X} variant='ghost' size='sm' />
          </Dialog.Close>
        </div>
        <Dialog.Description className='text-[15px] text-black mb-[15px]'>
          Select a collection to add this recipe to.
        </Dialog.Description>
        <div className='max-h-[400px] flex flex-col justify-start items-start w-full overflow-y-scroll'>
          {feedCollections.map((collection) => (
            <div key={collection.collection_id} onClick={(event:React.MouseEvent<HTMLDivElement>) => addToMyCollection(collection.collection_id)} className='bg-transparent border-none cursor-pointer flex flex-col gap-4 mb-6'>
              <div className='flex flex-row items-start gap-3'>
              <Image
                      src={collection.collection_image}
                      height={100}
                      width={100}
                      alt='thumbnail'
                      className='rounded-lg'
                    />
              <div className='flex flex-col items-start w-full'>

                <Paragraph className='text-black font-bold text-start mb-1'>
                  {collection.collection_name}
                </Paragraph>
                <Paragraph size='sm' className='text-start'>
                  {collection.description?.slice(0, 50) + (collection.description?.length > 50 ? '...' : '')}
                </Paragraph>
              </div>
            </div>
          </div>
          ))}
        </div>
      </Dialog.Content>
    </Dialog.Portal>
  </Dialog.Root>
)};

export default AddToCollectionDialog
