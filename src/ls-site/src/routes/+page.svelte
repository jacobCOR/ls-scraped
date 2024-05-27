<script>
    import SearchBar from '../components/SearchBar.svelte';
    import { goto } from '$app/navigation';

    const handleSearch = (event) => {
        const query = event.detail.query;
        goto(`/characters?name=${query}`);
    };
</script>

<h1>Linkshell Search</h1>
<SearchBar on:search={handleSearch}/>
