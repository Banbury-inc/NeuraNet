
            /// Returns the `rustc` SemVer version and additional metadata
            /// like the git short hash and build date.
            pub fn version_meta() -> VersionMeta {
                VersionMeta {
                    semver: Version {
                        major: 1,
                        minor: 78,
                        patch: 0,
                        pre: vec![],
                        build: vec![],
                    },
                    host: "x86_64-unknown-linux-gnu".to_owned(),
                    short_version_string: "rustc 1.78.0 (9b00956e5 2024-04-29)".to_owned(),
                    commit_hash: Some("9b00956e56009bab2aa15d7bff10916599e3d6d6".to_owned()),
                    commit_date: Some("2024-04-29".to_owned()),
                    build_date: None,
                    channel: Channel::Stable,
                }
            }
            