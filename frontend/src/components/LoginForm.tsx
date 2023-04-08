'use client'

import * as Form from '@radix-ui/react-form';
import { Button } from '@/ui/Button';
import { useRouter } from 'next/navigation';

const LoginForm = () => {

  const router = useRouter()

  async function submitForm(data) {
    const response = await fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const json = await response.json();
    alert(json.message)
    if (response.ok) {
      router.push('/');
    }
  }
  return (
    <Form.Root className='w-[360px] items-center px-8 md:px-0 pb-8'
      onSubmit={(event) => {
        const data = Object.fromEntries(new FormData(event.currentTarget));
        submitForm(data);
        event.preventDefault();
      }}
    >
      <Form.Field className='grid mb-[10px]' name='username'>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
            Username
          </Form.Label>
          <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
            Please enter your username
          </Form.Message>
        </div>
        <Form.Control asChild>
          <input
          className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
          type='text'
          required />
        </Form.Control>
      </Form.Field>
      <Form.Field className='grid mb-[15px]' name='password'>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
            Password
          </Form.Label>
        </div>
        <Form.Control asChild>
          <input
          className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black] selection:color-white'
          type='password'
          required />
        </Form.Control>
      </Form.Field>
      <Form.Submit asChild>
        <Button className='w-full'>
          Login
        </Button>
      </Form.Submit>
    </Form.Root>
  )
};

export default LoginForm
