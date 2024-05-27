export async function load({ url }) {
    const searchParams = new URLSearchParams(url.search);
    const char_name = searchParams.get('name') || '';
    console.log('Load function called with char_name:', char_name);

    return { props: { char_name } };
}