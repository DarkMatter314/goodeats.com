async function getRecipeById(id: string) {
  const res = await fetch(`${process.env.BASE_API_URL}/recipe/${id}`);
  const data = await res.json();
  return data;
}

export async function generateMetadata({ params }) {
  const postPromise = getRecipeById(params.id);
  const [post] = await Promise.all([postPromise]);
  if (post.recipe_data?.name) {
    return {
      title: `Goodeats | ${post.recipe_data.name}`,
    };
  } else {
    return {
      title: `Goodeats | Recipe not found`,
    }
  }
}

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <main>
      {children}
    </main>
  )
}
