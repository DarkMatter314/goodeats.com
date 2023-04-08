import * as Dialog from '@radix-ui/react-dialog';
import Paragraph from '@/ui/Paragraph';
import Icons from '@/components/Icons';
import { IconButton } from '@/components/ui/Button';
import { feedCollections } from '@/public/data';
// import { useRouter } from 'next/navigation';

const AddToCollectionDialog = () => {

  // const router = useRouter();

  const addToCollection = (collectionId: number) => (event: React.MouseEvent<HTMLDivElement>) => {
    event.preventDefault();
    // router.push(`/collections`);
  };

  return (
  <Dialog.Root>
    <Dialog.Trigger asChild>
      <IconButton icon={Icons.Plus} variant='ghost' className='hover:bg-purple-700' />
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
            <div key={collection.collectionId} onClick={addToCollection(collection.collectionId)} className='bg-transparent border-none cursor-pointer flex flex-col gap-4 mb-6'>
              <div className='flex flex-col items-start w-full'>
                <Paragraph className='text-black font-bold text-start'>
                  {collection.name}
                </Paragraph>
                <Paragraph size='sm' className='text-start'>
                  {collection.description}
                </Paragraph>
              </div>
            </div>
          ))}
        </div>
      </Dialog.Content>
    </Dialog.Portal>
  </Dialog.Root>
)};

export default AddToCollectionDialog
