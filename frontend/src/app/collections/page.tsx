import LargeHeading from '@/components/ui/LargeHeading';
import Paragraph from '@/components/ui/Paragraph';
import Image from 'next/image';
import { feedCollections } from '@/public/data';
import { Metadata } from 'next'
import NewCollectionDialog from '@/components/NewCollectionDialog';

export const metadata: Metadata = {
  title: 'Goodeats | My Collections',
}

const page: React.FC = () => {
  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden pb-32'>
      <div className='container pt-32 max-w-7xl mx-auto w-full h-full'>
        <div className='h-full gap-8 flex flex-col justify-start items-center'>
          <div className='flex flex-row items-center gap-6'>
            <LargeHeading>
              My Collections
            </LargeHeading>
            <NewCollectionDialog />
          </div>
          <div className='h-full flex flex-col justify-start items-center w-full px-8'>
            {feedCollections.map((collection) => (
              <div key={collection.collectionId} className='flex flex-col items-center md:items-start md:flex-row gap-4 md:w-[720px] lg:w-[900px] max-w-7xl pb-6'>
                <div className=''>
                  <Image
                    src={collection.imageUrl}
                    height={250}
                    width={250}
                    alt='thumbnail'
                    className='rounded-xl'
                  />
                </div>
                <div className='flex flex-col gap-1 w-[250px] md:w-full'>
                  <LargeHeading className='text-start' size='xs'>
                    {collection.name}
                  </LargeHeading>
                  <Paragraph size='sm' className='text-start'>
                    {collection.description}
                  </Paragraph>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default page
