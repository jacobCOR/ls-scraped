<form class="search-bar" on:submit={handleSubmit}>
    <input type="text" bind:value={query} placeholder="Search Character Name">
    <button type="submit">Search</button>
</form>

<style>
    .search-bar {
        display: flex;
        align-items: center;
    }
    input[type="text"] {
        flex: 1;
        padding: 0.5em;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    button {
        padding: 0.5em 1em;
        margin-left: 0.5em;
        border: none;
        background-color: #007BFF;
        color: white;
        border-radius: 4px;
        cursor: pointer;
    }
    button:hover {
        background-color: #0056b3;
    }
</style>

<script>
    import { createEventDispatcher } from 'svelte';

    let query = '';
    const dispatch = createEventDispatcher();


    const handleSubmit = (event) => {
        event.preventDefault();
        dispatch('search', { query });
    };
</script>
