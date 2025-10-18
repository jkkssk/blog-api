# ERD Diagram for Blog Database

```mermaid
erDiagram
    users {
        bigint id PK
        varchar username
        varchar email
        varchar password_hash
        timestamp created_at
        timestamp updated_at
    }

    posts {
        bigint id PK
        bigint author_id FK
        varchar title
        text content
        int likes_count
        int ratings_count
        decimal average_rating
        timestamp created_at
        timestamp updated_at
    }

    categories {
        bigint id PK
        varchar name
        text description
    }

    comments {
        bigint id PK
        bigint post_id FK
        bigint user_id FK
        bigint parent_comment_id FK
        text content
        timestamp created_at
        timestamp updated_at
    }

    users ||--o{ posts : writes
    users ||--o{ comments : writes
    users ||--o{ favorites : saves
    users ||--o{ subscriptions : subscribes
    users ||--o{ post_likes : likes
    users ||--o{ post_ratings : rates
    posts ||--o{ comments : has
    posts ||--o{ favorites : saved_in
    posts ||--o{ post_likes : liked_by
    posts ||--o{ post_ratings : rated_by
    posts }o--o{ categories : categorized_by
    comments ||--o{ comments : replies_to
