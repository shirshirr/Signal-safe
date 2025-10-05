import torch
import torch.nn as nn

class TinyTemporalFusion(nn.Module):
    def __init__(self, ts_input_dim, embed_dim, hidden=64):
        super().__init__()
        self.ts_encoder = nn.GRU(ts_input_dim, hidden, batch_first=True)
        self.embed_proj = nn.Linear(embed_dim, hidden)
        self.combine_fc = nn.Sequential(
            nn.Linear(hidden*2, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1),
            nn.Sigmoid()
        )
    def forward(self, ts, embeds):
        _, h = self.ts_encoder(ts)
        h = h.squeeze(0)
        e = self.embed_proj(embeds.mean(dim=1))
        x = torch.cat([h, e], dim=-1)
        return self.combine_fc(x).squeeze(-1)
