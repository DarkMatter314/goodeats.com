'use client'

import * as Form from '@radix-ui/react-form';
import * as Dialog from '@radix-ui/react-dialog';
import { Button } from '@/ui/Button';
import Icons from '@/components/Icons';
import { IconButton } from '@/components/ui/Button';

const NewCollectionDialog = () => {
  return (
  <Dialog.Root>
    <Dialog.Trigger asChild>
      <IconButton icon={Icons.Plus} variant='ghost' size='lg' />
    </Dialog.Trigger>
    <Dialog.Portal>
      <Dialog.Overlay className='bg-blackA9 data-[state=open]:animate-overlayShow fixed inset-0' />
      <Dialog.Content className="data-[state=open]:animate-contentShow fixed top-[50%] left-[50%] max-h-[85vh] w-[90vw] max-w-[450px] translate-x-[-50%] translate-y-[-50%] rounded-[6px] bg-white p-[25px] shadow-[hsl(206_22%_7%_/_35%)_0px_10px_38px_-10px,_hsl(206_22%_7%_/_20%)_0px_10px_20px_-15px] focus:outline-none">
        <div className='flex flex-row justify-between'>
          <Dialog.Title className='text-[20px] font-bold text-black mb-[15px]'>
            New collection
          </Dialog.Title>
          <Dialog.Close asChild>
            <IconButton icon={Icons.X} variant='ghost' size='sm' />
          </Dialog.Close>
        </div>
        <Dialog.Description className='text-[15px] text-black mb-[15px]'>
          Create a new collection to organize your recipes.
        </Dialog.Description>
        <Form.Root className='w-full flex flex-col items-start justify-start'>
          <Form.Field className='w-full grid mb-[10px]' name='collectionName'>
            <div className='flex items-baseline justify-between'>
              <Form.Label className='text-black font-medium text-[15px]'>
                Collection Name
              </Form.Label>
              <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
                Please provide a name
              </Form.Message>
            </div>
            <Form.Control asChild>
              <input className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black] selection:color-white' />
            </Form.Control>
          </Form.Field>
          <Form.Field className='w-full grid mb-[15px]' name='description'>
            <div className='flex items-baseline justify-between'>
              <Form.Label className='text-black font-medium text-[15px]'>
                Description
              </Form.Label>
            </div>
            <Form.Control asChild>
              <textarea className='pt-1 box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[80px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black] selection:color-white' />
            </Form.Control>
          </Form.Field>
          <div className='flex flex-row w-full justify-end'>
            <Form.Submit asChild>
              <Button className='w-full md:w-2/5'>
                Add
              </Button>
            </Form.Submit>
          </div>
        </Form.Root>
      </Dialog.Content>
    </Dialog.Portal>
  </Dialog.Root>
)};

export default NewCollectionDialog
